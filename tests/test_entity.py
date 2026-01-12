"""
Tests pour la classe Entity
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity
import numpy as np

def test_entity_creation():
    """Test création basique"""
    e = Entity(10.0)
    assert e.state[0] == 10.0
    assert e.mass == 1.0
    assert not e.is_frozen
    print("✅ test_entity_creation")

def test_entity_multidim():
    """Test entité multidimensionnelle"""
    e = Entity([1.0, 2.0, 3.0])
    assert len(e.state) == 3
    assert e.state[0] == 1.0
    assert e.state[2] == 3.0
    print("✅ test_entity_multidim")

def test_entity_freeze():
    """Test freeze/unfreeze"""
    e = Entity(5.0)
    e.velocity = np.array([1.0])
    
    assert not e.is_frozen
    e.freeze()
    assert e.is_frozen
    assert e.velocity[0] == 0.0
    
    e.unfreeze()
    assert not e.is_frozen
    print("✅ test_entity_freeze")

def test_entity_distance():
    """Test calcul distance"""
    e1 = Entity(0.0)
    e2 = Entity(3.0)
    
    dist = e1.distance_to(e2)
    assert abs(dist - 3.0) < 0.001
    print("✅ test_entity_distance")

def test_entity_copy():
    """Test copie"""
    e1 = Entity(10.0, mass=2.0, properties={'id': 1})
    e2 = e1.copy()
    
    assert e2.state[0] == e1.state[0]
    assert e2.mass == e1.mass
    assert e2.properties['id'] == 1
    assert e2.id != e1.id  # IDs différents
    print("✅ test_entity_copy")

def test_entity_properties():
    """Test propriétés custom"""
    e = Entity(5.0, properties={'name': 'test', 'value': 42})
    assert e.properties['name'] == 'test'
    assert e.properties['value'] == 42
    print("✅ test_entity_properties")

def main():
    print("="*70)
    print("Tests Entity")
    print("="*70 + "\n")
    
    test_entity_creation()
    test_entity_multidim()
    test_entity_freeze()
    test_entity_distance()
    test_entity_copy()
    test_entity_properties()
    
    print("\n" + "="*70)
    print("✅ Tous les tests Entity passés")
    print("="*70)

if __name__ == "__main__":
    main()