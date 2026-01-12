"""
Tests pour la classe System
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, System, Force, Topology
import numpy as np

def test_system_creation():
    """Test création système"""
    entities = [Entity(float(i)) for i in range(10)]
    system = System(entities)
    
    assert len(system.entities) == 10
    assert system.momentum == 0.8
    assert system.freeze_enabled == True
    print("✅ test_system_creation")

def test_system_step():
    """Test exécution step"""
    entities = [Entity(float(i * 10)) for i in range(5)]
    system = System(entities, force=Force.attraction(0.5))
    
    initial_var = system.variance()
    system.step()
    
    assert system.step_count == 1
    print("✅ test_system_step")

def test_system_convergence():
    """Test convergence"""
    entities = [Entity(float(i * 10)) for i in range(10)]
    system = System(
        entities,
        force=Force.attraction(0.5),
        topology=Topology.full()
    )
    
    initial_var = system.variance()
    system.run(steps=50)
    final_var = system.variance()
    
    assert final_var < initial_var
    print("✅ test_system_convergence")

def test_system_freeze():
    """Test mécanisme freeze"""
    entities = [Entity(float(i)) for i in range(5)]
    system = System(
        entities,
        force=Force.attraction(0.5),
        freeze_enabled=True
    )
    
    system.run(steps=100)
    
    frozen_ratio = system.frozen_ratio()
    assert frozen_ratio > 0.0
    print(f"✅ test_system_freeze (gelées: {frozen_ratio*100:.0f}%)")

def test_system_variance():
    """Test calcul variance"""
    entities = [Entity(0.0), Entity(10.0)]
    system = System(entities)
    
    var = system.variance()
    assert var > 0
    print("✅ test_system_variance")

def test_system_states():
    """Test get_states"""
    entities = [Entity(float(i)) for i in range(5)]
    system = System(entities)
    
    states = system.get_states()
    assert len(states) == 5
    assert states[0] == 0.0
    assert states[4] == 4.0
    print("✅ test_system_states")

def main():
    print("="*70)
    print("Tests System")
    print("="*70 + "\n")
    
    test_system_creation()
    test_system_step()
    test_system_convergence()
    test_system_freeze()
    test_system_variance()
    test_system_states()
    
    print("\n" + "="*70)
    print("✅ Tous les tests System passés")
    print("="*70)

if __name__ == "__main__":
    main()