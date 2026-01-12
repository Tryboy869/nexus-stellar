"""
Exemple: Tri Distribué
Démontre le tri émergent par attracteurs discrets
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, System, Force, Topology, Attractor
import random
import time

def main():
    print("="*70)
    print("NEXUS-STELLAR: Tri Émergent")
    print("="*70 + "\n")
    
    # Liste à trier
    data = [8, 3, 9, 1, 5, 2, 7, 4, 6]
    print(f"📊 Liste à trier: {data}\n")
    
    # Création entités
    entities = [
        Entity(
            state=float(i),
            properties={'value': val, 'original_index': i}
        )
        for i, val in enumerate(data)
    ]
    
    # Attracteurs (positions cibles)
    attractors = [
        Attractor(position=float(i), strength=0.3)
        for i in range(len(data))
    ]
    
    # Système de tri
    print("🔄 Création système de tri...")
    system = System(
        entities=entities,
        force=Force.attraction(0.3),
        topology=Topology.ring(),
        momentum=0.8,
        freeze_enabled=True
    )
    
    # Ajout attracteurs
    for att in attractors:
        system.add_attractor(att)
    
    # Exécution
    print("🚀 Démarrage tri émergent...\n")
    start_time = time.time()
    
    for step in range(100):
        system.step()
        
        if step % 20 == 0:
            print(f"   Step {step:3d} | Variance: {system.variance():8.4f}")
    
    duration = (time.time() - start_time) * 1000
    
    # Extraction résultat
    sorted_entities = sorted(entities, key=lambda e: e.state[0])
    sorted_values = [e.properties['value'] for e in sorted_entities]
    
    # Résultats
    print("\n" + "="*70)
    print("RÉSULTATS")
    print("="*70)
    
    print(f"📥 Liste originale:  {data}")
    print(f"📤 Liste triée:      {sorted_values}")
    print(f"✅ Tri correct:      {sorted_values == sorted(data)}")
    print(f"⏱️  Temps:            {duration:.2f}ms")
    print(f"📈 Steps:            {system.step_count}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()