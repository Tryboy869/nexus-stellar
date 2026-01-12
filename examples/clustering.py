"""
Exemple: Clustering de Données
Démontre la compression par fusion sémantique
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, FusionEngine
import numpy as np
import time

def main():
    print("="*70)
    print("NEXUS-STELLAR: Clustering par Fusion")
    print("="*70 + "\n")
    
    # Génération dataset avec clusters naturels
    print("📊 Génération de 1000 vecteurs en 4 clusters...")
    
    clusters_data = []
    
    # Cluster 1: Autour de [1, 1, 1, ...]
    for _ in range(250):
        vec = np.random.normal(1.0, 0.2, 10)
        clusters_data.append(vec)
    
    # Cluster 2: Autour de [5, 5, 5, ...]
    for _ in range(250):
        vec = np.random.normal(5.0, 0.2, 10)
        clusters_data.append(vec)
    
    # Cluster 3: Autour de [10, 10, 10, ...]
    for _ in range(250):
        vec = np.random.normal(10.0, 0.2, 10)
        clusters_data.append(vec)
    
    # Cluster 4: Autour de [15, 15, 15, ...]
    for _ in range(250):
        vec = np.random.normal(15.0, 0.2, 10)
        clusters_data.append(vec)
    
    # Création entités
    entities = [Entity(vec) for vec in clusters_data]
    print(f"   Total vecteurs: {len(entities)}")
    print(f"   Dimensions: {len(entities[0].state)}\n")
    
    # Fusion
    print("🔥 Démarrage fusion solaire...")
    start_time = time.time()
    
    fusion = FusionEngine(threshold=1.0, method='euclidean')
    compressed = fusion.compress(entities)
    
    duration = (time.time() - start_time) * 1000
    
    # Analyse résultats
    print("\n" + "="*70)
    print("RÉSULTATS")
    print("="*70)
    
    print(f"📉 Réduction: {len(entities)} → {len(compressed)} clusters")
    print(f"📊 Taux compression: {(1 - len(compressed)/len(entities))*100:.1f}%")
    print(f"⏱️  Temps: {duration:.2f}ms\n")
    
    # Détails des clusters
    print("🔍 Analyse des clusters:")
    compressed_sorted = sorted(compressed, key=lambda c: c.mass, reverse=True)
    
    for i, cluster in enumerate(compressed_sorted[:10]):
        centroid_preview = cluster.state[:3]
        print(f"   Cluster {i+1}: {cluster.mass:4.0f} points | "
              f"Centroïde: [{', '.join(f'{x:.2f}' for x in centroid_preview)}, ...]")
    
    if len(compressed_sorted) > 10:
        print(f"   ... et {len(compressed_sorted) - 10} autres clusters")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()