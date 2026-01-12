"""
NEXUS-STELLAR v0.1.0
Moteur de calcul émergent polyglotte auto-compilant

Auteur: Daouda Abdoul Anzize
Organisation: Nexus Studio
Contact: nexusstudio100@gmail.com
GitHub: https://github.com/Tryboy869/nexus-stellar
License: MIT

Changelog v0.1.0:
- Version initiale
- Primitives de base (Entity, Force, Topology, System, FusionEngine)
- Support Rust + C++ auto-compilés
- Cache intelligent
"""

import subprocess
import ctypes
import numpy as np
import os
import sys
from pathlib import Path
import hashlib
import time
import json
from typing import List, Dict, Any, Callable, Optional, Union
import warnings

# ============================================================
# SOURCES RUST
# ============================================================

RUST_SOURCE = """
use std::slice;
use rayon::prelude::*;

#[no_mangle]
pub extern "C" fn nexus_step(
    states: *mut f32,
    velocities: *mut f32,
    frozen: *mut u8,
    neighbors: *const i32,
    neighbor_counts: *const i32,
    n_entities: usize,
    momentum: f32,
    force_strength: f32
) {
    let states = unsafe { slice::from_raw_parts_mut(states, n_entities) };
    let velocities = unsafe { slice::from_raw_parts_mut(velocities, n_entities) };
    let frozen = unsafe { slice::from_raw_parts_mut(frozen, n_entities) };
    
    // Calcul des forces en parallèle avec Rayon
    let forces: Vec<f32> = (0..n_entities).into_par_iter().map(|i| {
        if frozen[i] == 1 {
            return 0.0;
        }
        
        let n_neigh = unsafe { *neighbor_counts.add(i) as usize };
        let offset: usize = (0..i).map(|j| unsafe { *neighbor_counts.add(j) as usize }).sum();
        let neigh_slice = unsafe { slice::from_raw_parts(neighbors.add(offset), n_neigh) };
        
        let mut force = 0.0f32;
        for &j in neigh_slice {
            let j = j as usize;
            if j < n_entities {
                force += (states[j] - states[i]) * force_strength;
            }
        }
        
        if n_neigh > 0 {
            force / n_neigh as f32
        } else {
            0.0
        }
    }).collect();
    
    // Application des forces (séquentiel pour éviter race conditions)
    for i in 0..n_entities {
        if frozen[i] == 0 {
            velocities[i] = momentum * velocities[i] + (1.0 - momentum) * forces[i];
            states[i] += velocities[i];
        }
    }
}

#[no_mangle]
pub extern "C" fn nexus_variance(states: *const f32, n: usize) -> f32 {
    let states = unsafe { slice::from_raw_parts(states, n) };
    let mean: f32 = states.iter().sum::<f32>() / n as f32;
    states.iter().map(|s| (s - mean).powi(2)).sum::<f32>() / n as f32
}
"""

# ============================================================
# SOURCES C++
# ============================================================

CPP_SOURCE = """
#include <cmath>
#include <vector>
#include <algorithm>

extern "C" {

struct FusionNode {
    float* state;
    int dim;
    float mass;
    int id;
    bool absorbed;
};

void fusion_compress(
    float* states,
    int* ids,
    float* masses,
    int* n_nodes,
    int dim,
    float threshold
) {
    std::vector<FusionNode> nodes;
    
    for (int i = 0; i < *n_nodes; i++) {
        FusionNode node;
        node.state = &states[i * dim];
        node.dim = dim;
        node.mass = masses[i];
        node.id = ids[i];
        node.absorbed = false;
        nodes.push_back(node);
    }
    
    bool fused = true;
    int iterations = 0;
    
    // Optimisation: Marquage au lieu d'erase (évite O(N²))
    while (fused && iterations < 20) {
        fused = false;
        
        for (size_t i = 0; i < nodes.size(); i++) {
            if (nodes[i].absorbed) continue;
            
            for (size_t j = i + 1; j < nodes.size(); j++) {
                if (nodes[j].absorbed) continue;
                
                float dist_sq = 0.0f;
                
                for (int k = 0; k < dim; k++) {
                    float diff = nodes[i].state[k] - nodes[j].state[k];
                    dist_sq += diff * diff;
                }
                
                if (std::sqrt(dist_sq) < threshold) {
                    float total_mass = nodes[i].mass + nodes[j].mass;
                    
                    for (int k = 0; k < dim; k++) {
                        nodes[i].state[k] = (
                            nodes[i].state[k] * nodes[i].mass +
                            nodes[j].state[k] * nodes[j].mass
                        ) / total_mass;
                    }
                    
                    nodes[i].mass = total_mass;
                    nodes[j].absorbed = true;
                    fused = true;
                    break;
                }
            }
        }
        iterations++;
    }
    
    // Compaction finale
    int write_idx = 0;
    for (size_t i = 0; i < nodes.size(); i++) {
        if (!nodes[i].absorbed) {
            for (int k = 0; k < dim; k++) {
                states[write_idx * dim + k] = nodes[i].state[k];
            }
            ids[write_idx] = nodes[i].id;
            masses[write_idx] = nodes[i].mass;
            write_idx++;
        }
    }
    
    *n_nodes = write_idx;
}

}
"""

# ============================================================
# COMPILATION MANAGER
# ============================================================

class CompilerManager:
    def __init__(self):
        self.cache_dir = Path.home() / ".nexus_stellar_cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.rust_lib = None
        self.cpp_lib = None
    
    def _hash_source(self, source: str) -> str:
        return hashlib.sha256(source.encode()).hexdigest()[:16]
    
    def _needs_recompile(self, source: str, lib_name: str) -> bool:
        hash_file = self.cache_dir / f"{lib_name}.hash"
        lib_file = self.cache_dir / f"{lib_name}.so"
        
        if not hash_file.exists() or not lib_file.exists():
            return True
        
        current_hash = self._hash_source(source)
        stored_hash = hash_file.read_text()
        return current_hash != stored_hash
    
    def compile_rust(self, source: str, lib_name: str = "nexus_rust"):
        if not self._needs_recompile(source, lib_name):
            print(f"♻️  Cache Rust ({lib_name})")
            self.rust_lib = ctypes.CDLL(str(self.cache_dir / f"{lib_name}.so"))
            return self.rust_lib
        
        print(f"🦀 Compilation Rust (avec Rayon)...")
        
        rs_file = self.cache_dir / f"{lib_name}.rs"
        rs_file.write_text(source)
        
        # Cargo.toml pour Rayon
        cargo_toml = self.cache_dir / "Cargo.toml"
        cargo_toml.write_text("""
[package]
name = "nexus_rust"
version = "0.1.0"
edition = "2021"

[dependencies]
rayon = "1.8"

[lib]
crate-type = ["cdylib"]
path = "nexus_rust.rs"
""")
        
        # Compilation avec Cargo
        result = subprocess.run([
            "cargo", "build", "--release",
            "--manifest-path", str(cargo_toml)
        ], capture_output=True, text=True, cwd=str(self.cache_dir))
        
        if result.returncode != 0:
            # Fallback: compilation sans Rayon si cargo pas dispo
            print("⚠️  Cargo non disponible, compilation rustc simple...")
            result = subprocess.run([
                "rustc", "--crate-type=cdylib", "-C", "opt-level=3",
                str(rs_file), "-o", str(self.cache_dir / f"{lib_name}.so")
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"Erreur Rust:\n{result.stderr}")
        else:
            # Copie depuis target/release
            import shutil
            lib_path = self.cache_dir / "target" / "release" / f"lib{lib_name}.so"
            if lib_path.exists():
                shutil.copy(lib_path, self.cache_dir / f"{lib_name}.so")
        
        hash_file = self.cache_dir / f"{lib_name}.hash"
        hash_file.write_text(self._hash_source(source))
        
        self.rust_lib = ctypes.CDLL(str(self.cache_dir / f"{lib_name}.so"))
        print("✅ Rust OK")
        return self.rust_lib
    
    def compile_cpp(self, source: str, lib_name: str = "nexus_cpp"):
        if not self._needs_recompile(source, lib_name):
            print(f"♻️  Cache C++ ({lib_name})")
            self.cpp_lib = ctypes.CDLL(str(self.cache_dir / f"{lib_name}.so"))
            return self.cpp_lib
        
        print(f"⚡ Compilation C++...")
        
        cpp_file = self.cache_dir / f"{lib_name}.cpp"
        cpp_file.write_text(source)
        
        result = subprocess.run([
            "g++", "-shared", "-fPIC", "-O3", "-march=native",
            str(cpp_file), "-o", str(self.cache_dir / f"{lib_name}.so")
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Erreur C++:\n{result.stderr}")
        
        hash_file = self.cache_dir / f"{lib_name}.hash"
        hash_file.write_text(self._hash_source(source))
        
        self.cpp_lib = ctypes.CDLL(str(self.cache_dir / f"{lib_name}.so"))
        print("✅ C++ OK")
        return self.cpp_lib

# ============================================================
# ENTITY
# ============================================================

class Entity:
    _id_counter = 0
    
    def __init__(self, state: Union[float, List[float]], 
                 mass: float = 1.0, charge: float = 0.0,
                 velocity: Union[float, List[float]] = None,
                 properties: Dict = None):
        self.id = Entity._id_counter
        Entity._id_counter += 1
        
        self.state = np.array([state] if isinstance(state, (int, float)) else state, dtype=np.float32)
        self.mass = float(mass)
        self.charge = float(charge)
        self.velocity = np.zeros_like(self.state) if velocity is None else np.array(velocity, dtype=np.float32)
        self.is_frozen = False
        self.properties = properties or {}
        self.stability_counter = 0
    
    def freeze(self):
        self.is_frozen = True
        self.velocity = np.zeros_like(self.velocity)
    
    def unfreeze(self):
        self.is_frozen = False
        self.stability_counter = 0
    
    def distance_to(self, other: 'Entity') -> float:
        return float(np.linalg.norm(self.state - other.state))
    
    def copy(self) -> 'Entity':
        e = Entity(self.state.copy(), self.mass, self.charge, 
                   self.velocity.copy(), self.properties.copy())
        e.is_frozen = self.is_frozen
        return e

# ============================================================
# FORCE
# ============================================================

class Force:
    def __init__(self, func: Callable):
        self.func = func
    
    @staticmethod
    def attraction(strength: float = 0.5):
        def f(e1, e2):
            return (e2.state - e1.state) * strength
        return Force(f)
    
    @staticmethod
    def repulsion(strength: float = 0.3):
        def f(e1, e2):
            diff = e2.state - e1.state
            dist = np.linalg.norm(diff)
            if dist < 0.01:
                dist = 0.01
            return -diff * strength / dist
        return Force(f)
    
    @staticmethod
    def gravity(G: float = 1.0):
        def f(e1, e2):
            diff = e2.state - e1.state
            dist = np.linalg.norm(diff)
            if dist < 0.01:
                dist = 0.01
            force_mag = G * e1.mass * e2.mass / (dist ** 2)
            return diff / dist * force_mag
        return Force(f)
    
    @staticmethod
    def spring(k: float = 0.8, rest_length: float = 0.0):
        def f(e1, e2):
            diff = e2.state - e1.state
            dist = np.linalg.norm(diff)
            displacement = dist - rest_length
            return diff / dist * k * displacement if dist > 0 else 0
        return Force(f)
    
    @staticmethod
    def custom(func: Callable):
        return Force(func)
    
    def compute(self, e1: Entity, e2: Entity):
        return self.func(e1, e2)

# ============================================================
# TOPOLOGY
# ============================================================

class Topology:
    def __init__(self, func: Callable):
        self.func = func
    
    @staticmethod
    def small_world(shortcuts: int = 2, k: int = 2):
        def f(entity_id, entities):
            n = len(entities)
            neighbors = [(entity_id - 1) % n, (entity_id + 1) % n]
            
            import random
            for _ in range(shortcuts):
                j = random.randint(0, n - 1)
                if j != entity_id and j not in neighbors:
                    neighbors.append(j)
            
            return neighbors
        return Topology(f)
    
    @staticmethod
    def ring():
        def f(entity_id, entities):
            n = len(entities)
            return [(entity_id - 1) % n, (entity_id + 1) % n]
        return Topology(f)
    
    @staticmethod
    def full():
        def f(entity_id, entities):
            return [e.id for e in entities if e.id != entity_id]
        return Topology(f)
    
    @staticmethod
    def grid_2d(width: int, height: int = None):
        if height is None:
            height = width
        
        def f(entity_id, entities):
            row, col = entity_id // width, entity_id % width
            neighbors = []
            
            if row > 0:
                neighbors.append((row - 1) * width + col)
            if row < height - 1:
                neighbors.append((row + 1) * width + col)
            if col > 0:
                neighbors.append(row * width + col - 1)
            if col < width - 1:
                neighbors.append(row * width + col + 1)
            
            return neighbors
        return Topology(f)
    
    @staticmethod
    def custom(func: Callable):
        return Topology(func)
    
    def get_neighbors(self, entity_id: int, entities: List[Entity]) -> List[int]:
        return self.func(entity_id, entities)

# ============================================================
# SYSTEM
# ============================================================

class System:
    def __init__(self, entities: List[Entity],
                 force: Force = None,
                 topology: Topology = None,
                 momentum: float = 0.8,
                 freeze_enabled: bool = True,
                 freeze_threshold: float = 0.01,
                 freeze_stability_steps: int = 5):
        
        self.entities = entities
        self.force = force or Force.attraction(0.5)
        self.topology = topology or Topology.small_world()
        self.momentum = momentum
        self.freeze_enabled = freeze_enabled
        self.freeze_threshold = freeze_threshold
        self.freeze_stability_steps = freeze_stability_steps
        self.attractors = []
        self.observers = []
        self.step_count = 0
        
        # Compilation
        self.compiler = CompilerManager()
        self._bootstrap()
    
    def _bootstrap(self):
        rust_lib = self.compiler.compile_rust(RUST_SOURCE)
        
        rust_lib.nexus_step.argtypes = [
            ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t,
            ctypes.c_float, ctypes.c_float
        ]
        
        rust_lib.nexus_variance.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_size_t]
        rust_lib.nexus_variance.restype = ctypes.c_float
        
        self.rust = rust_lib
    
    def step(self):
        n = len(self.entities)
        
        states = np.array([e.state[0] if len(e.state) == 1 else e.state[0] 
                          for e in self.entities], dtype=np.float32)
        velocities = np.array([e.velocity[0] if len(e.velocity) == 1 else e.velocity[0]
                              for e in self.entities], dtype=np.float32)
        frozen = np.array([1 if e.is_frozen else 0 for e in self.entities], dtype=np.uint8)
        
        all_neighbors = []
        neighbor_counts = []
        
        for e in self.entities:
            neighbors = self.topology.get_neighbors(e.id, self.entities)
            all_neighbors.extend(neighbors)
            neighbor_counts.append(len(neighbors))
        
        neighbors_arr = np.array(all_neighbors, dtype=np.int32)
        counts_arr = np.array(neighbor_counts, dtype=np.int32)
        
        self.rust.nexus_step(
            states.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            velocities.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            frozen.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
            neighbors_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            counts_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            n, self.momentum, 0.5
        )
        
        for i, e in enumerate(self.entities):
            if not e.is_frozen:
                e.state[0] = states[i]
                e.velocity[0] = velocities[i]
                
                if abs(velocities[i]) < self.freeze_threshold:
                    e.stability_counter += 1
                    if e.stability_counter >= self.freeze_stability_steps:
                        e.freeze()
                else:
                    e.stability_counter = 0
        
        self.step_count += 1
        
        for obs in self.observers:
            obs._record(self)
    
    def run(self, steps: int = 100):
        for _ in range(steps):
            self.step()
    
    def run_until_stable(self, max_steps: int = 1000, threshold: float = 0.1):
        for _ in range(max_steps):
            self.step()
            if self.variance() < threshold:
                break
    
    def variance(self) -> float:
        states = np.array([e.state[0] for e in self.entities], dtype=np.float32)
        return float(self.rust.nexus_variance(
            states.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            len(states)
        ))
    
    def frozen_ratio(self) -> float:
        return sum(1 for e in self.entities if e.is_frozen) / len(self.entities)
    
    def get_states(self) -> List[float]:
        return [float(e.state[0]) for e in self.entities]
    
    def attach_observer(self, observer: 'Observer'):
        self.observers.append(observer)

# ============================================================
# FUSION ENGINE
# ============================================================

class FusionEngine:
    def __init__(self, threshold: float = 1.0, method: str = 'euclidean'):
        self.threshold = threshold
        self.method = method
        self.compiler = CompilerManager()
        self._bootstrap()
    
    def _bootstrap(self):
        cpp_lib = self.compiler.compile_cpp(CPP_SOURCE)
        
        cpp_lib.fusion_compress.argtypes = [
            ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int32),
            ctypes.c_int, ctypes.c_float
        ]
        
        self.cpp = cpp_lib
    
    def compress(self, entities: List[Entity]) -> List[Entity]:
        if not entities:
            return []
        
        dim = len(entities[0].state)
        n = len(entities)
        
        states = np.array([e.state for e in entities], dtype=np.float32).flatten()
        ids = np.array([e.id for e in entities], dtype=np.int32)
        masses = np.array([e.mass for e in entities], dtype=np.float32)
        n_nodes = np.array([n], dtype=np.int32)
        
        self.cpp.fusion_compress(
            states.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            ids.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            masses.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            n_nodes.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            dim, self.threshold
        )
        
        final_n = n_nodes[0]
        result = []
        
        for i in range(final_n):
            state = states[i * dim:(i + 1) * dim]
            result.append(Entity(state.tolist(), mass=masses[i]))
        
        return result

# ============================================================
# OBSERVER
# ============================================================

class Observer:
    def __init__(self, metrics: List[str] = None, frequency: int = 1):
        self.metrics = metrics or ['variance']
        self.frequency = frequency
        self.history = []
    
    def _record(self, system: System):
        if system.step_count % self.frequency != 0:
            return
        
        record = {'step': system.step_count}
        
        for metric in self.metrics:
            if metric == 'variance':
                record['variance'] = system.variance()
            elif metric == 'frozen_ratio':
                record['frozen_ratio'] = system.frozen_ratio()
        
        self.history.append(record)
    
    def get_history(self) -> List[Dict]:
        return self.history

# ============================================================
# ATTRACTOR
# ============================================================

class Attractor:
    def __init__(self, position: float, strength: float = 0.3):
        self.position = position
        self.strength = strength

# ============================================================
# DEMO
# ============================================================

def demo():
    print("="*70)
    print("NEXUS-STELLAR v1.0.0")
    print("="*70 + "\n")
    
    entities = [Entity(float(i * 10)) for i in range(10)]
    system = System(entities, momentum=0.8)
    
    print("📊 Test Consensus")
    print(f"   États initiaux: {system.get_states()[:5]}...")
    
    t0 = time.time()
    system.run(steps=50)
    t = (time.time() - t0) * 1000
    
    print(f"   ✨ Variance finale: {system.variance():.4f}")
    print(f"   ⏱️  Temps: {t:.2f}ms")
    print(f"   🧊 Gelées: {system.frozen_ratio()*100:.0f}%\n")
    
    print("="*70)

if __name__ == "__main__":
    demo()