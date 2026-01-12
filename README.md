# NEXUS-STELLAR

**Moteur de calcul émergent polyglotte auto-compilant**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🌌 Vision

Nexus-Stellar est un moteur de calcul qui résout des problèmes complexes par **émergence naturelle** plutôt que par algorithmes classiques. Inspiré des lois physiques universelles (convergence stellaire, fusion solaire), il fournit des **primitives** que les développeurs combinent librement.

**Créé par:** Daouda Abdoul Anzize  
**Organisation:** Nexus Studio  
**Contact:** nexusstudio100@gmail.com  
**GitHub:** [Tryboy869](https://github.com/Tryboy869)

---

## ⚡ Installation

### Via Docker (Recommandé)

```bash
git clone https://github.com/Tryboy869/nexus-stellar
cd nexus-stellar
docker build -t nexus-stellar .
docker run nexus-stellar
```

### Installation Locale

```bash
# Prérequis: Rust et C++
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
sudo apt install build-essential  # Linux
# brew install gcc  # macOS

pip install numpy
python nexus_stellar.py
```

---

## 🚀 Quick Start

```python
from nexus_stellar import Entity, System, Force, Topology

# Créer des entités
entities = [Entity(float(i * 10)) for i in range(50)]

# Système avec convergence
system = System(
    entities=entities,
    force=Force.attraction(0.5),
    topology=Topology.small_world(),
    momentum=0.8
)

# Exécution
system.run(steps=100)

print(f"Variance: {system.variance():.4f}")
print(f"Gelées: {system.frozen_ratio()*100:.0f}%")
```

---

## 🧱 Les 7 Primitives

### 1. **Entity** - Unité atomique
```python
entity = Entity(
    state=10.0,
    mass=1.0,
    properties={'type': 'player'}
)
```

### 2. **Force** - Loi d'interaction
```python
Force.attraction(0.5)
Force.repulsion(0.3)
Force.gravity(G=1.0)
Force.custom(lambda e1, e2: ...)
```

### 3. **Topology** - Réseau
```python
Topology.small_world()
Topology.ring()
Topology.full()
Topology.grid_2d(width=10)
```

### 4. **System** - Conteneur
```python
system = System(entities, force, topology)
system.run(steps=100)
```

### 5. **FusionEngine** - Compression
```python
fusion = FusionEngine(threshold=1.0)
compressed = fusion.compress(entities)
```

### 6. **Observer** - Monitoring
```python
observer = Observer(metrics=['variance'])
system.attach_observer(observer)
```

### 7. **Attractor** - Point fixe
```python
attractor = Attractor(position=50.0, strength=0.3)
system.add_attractor(attractor)
```

---

## 📚 Exemples

### Load Balancer
```python
servers = [Entity(load) for load in [10, 45, 23, 67]]
system = System(servers, Force.attraction(0.5), Topology.full())
system.run_until_stable()
```

### Physique de Jeu
```python
particles = [Entity([x, y]) for x, y in positions]
system = System(particles, Force.gravity(1.0), Topology.full())

for frame in range(1000):
    system.step()
    # render...
```

### Clustering
```python
entities = [Entity(vector) for vector in dataset]
fusion = FusionEngine(threshold=0.5)
clusters = fusion.compress(entities)
```

---

## 📖 Documentation

- [Quick Start](docs/quickstart.md)
- [Primitives Guide](docs/primitives.md)
- [Cookbook](docs/cookbook.md)
- [API Reference](docs/api-reference.md)

---

## 🎯 Cas d'Usage

- ✅ Load Balancing distribué
- ✅ Moteurs de jeu (physique)
- ✅ Machine Learning (clustering)
- ✅ Réseaux P2P
- ✅ Optimisation
- ✅ Consensus distribué

---

## 🧪 Tests

```bash
python -m pytest tests/
```

---

## 📄 License

MIT License - voir [LICENSE](LICENSE)

---

## 🤝 Contributing

Les contributions sont bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📧 Contact

**Daouda Abdoul Anzize**  
Nexus Studio  
nexusstudio100@gmail.com  
GitHub: [@Tryboy869](https://github.com/Tryboy869)