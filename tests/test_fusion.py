"""
Tests pour FusionEngine
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, FusionEngine
import numpy as np

def test_fusion_basic():
    """Test fusion basique"""
    entities = [
        Entity([1.0, 1.0]),
        Entity([1.1, 1.1]),
        Entity([10.0, 10.0])
    ]
    
    fusion = FusionEngine(threshold=0.5)
    compressed = fusion.compress(entities)
    
    assert len(compressed) < len(entities)
    print(f"✅ test_fusion_basic ({len(entities)} → {len(compressed)})")

def test_fusion_clusters():
    """Test fusion avec clusters distincts"""
    entities = []
    
    # Cluster 1
    for _ in range(10):
        entities.append(Entity(np.random.normal(0, 0.1, 5)))
    
    # Cluster 2
    for _ in range(10):
        entities.append(Entity(np.random.normal(10, 0.1, 5)))
    
    fusion = FusionEngine(threshold=1.0)
    compressed = fusion.compress(entities)
    
    assert len(compressed) <= 5  # Devrait avoir ~2 clusters
    print(f"✅ test_fusion_clusters ({len(entities)} → {len(compressed)})")

def test_fusion_mass():
    """Test conservation masse"""
    entities = [Entity([i]) for i in range(10)]
    
    initial_mass = sum(e.mass for e in entities)
    
    fusion = FusionEngine(threshold=2.0)
    compressed = fusion.compress(entities)
    
    final_mass = sum(e.mass for e in compressed)
    
    assert abs(final_mass - initial_mass) < 0.1
    print(f"✅ test_fusion_mass (masse: {initial_mass:.1f} → {final_mass:.1f})")

def test_fusion_no_fusion():
    """Test sans fusion (seuil très bas)"""
    entities = [Entity([i * 10]) for i in range(5)]
    
    fusion = FusionEngine(threshold=0.1)
    compressed = fusion.compress(entities)
    
    assert len(compressed) == len(entities)
    print("✅ test_fusion_no_fusion (aucune fusion)")

def main():
    print("="*70)
    print("Tests FusionEngine")
    print("="*70 + "\n")
    
    test_fusion_basic()
    test_fusion_clusters()
    test_fusion_mass()
    test_fusion_no_fusion()
    
    print("\n" + "="*70)
    print("✅ Tous les tests Fusion passés")
    print("="*70)

if __name__ == "__main__":
    main()