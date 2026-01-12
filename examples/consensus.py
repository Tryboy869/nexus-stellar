"""
Exemple: Consensus Distribué
Démontre comment 50 serveurs avec valeurs différentes convergent vers un consensus
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, System, Force, Topology, Observer
import random
import time

def main():
    print("="*70)
    print("NEXUS-STELLAR: Consensus Distribué")
    print("="*70 + "\n")
    
    # Création de 50 serveurs avec valeurs aléatoires
    print("📊 Initialisation de 50 serveurs...")
    servers = [
        Entity(
            state=random.uniform(0, 100),
            properties={'name': f'server-{i:02d}'}
        )
        for i in range(50)
    ]
    
    initial_states = [s.state[0] for s in servers]
    print(f"   États initiaux (premiers 10): {[f'{s:.1f}' for s in initial_states[:10]]}")
    print(f"   Variance initiale: {sum((s - sum(initial_states)/len(initial_states))**2 for s in initial_states)/len(initial_states):.2f}\n")
    
    # Création du système avec topologie Small-World
    print("🌐 Création système avec topologie Small-World...")
    system = System(
        entities=servers,
        force=Force.attraction(strength=0.5),
        topology=Topology.small_world(shortcuts=2),
        momentum=0.8,
        freeze_enabled=True,
        freeze_threshold=0.01,
        freeze_stability_steps=5
    )
    
    # Attachement observer
    observer = Observer(metrics=['variance', 'frozen_ratio'], frequency=5)
    system.attach_observer(observer)
    
    # Exécution
    print("🚀 Démarrage convergence...\n")
    start_time = time.time()
    
    for step in range(100):
        system.step()
        
        if step % 10 == 0:
            var = system.variance()
            frozen = system.frozen_ratio() * 100
            print(f"   Step {step:3d} | Variance: {var:8.4f} | Gelées: {frozen:5.1f}%")
        
        if system.variance() < 0.1:
            print(f"\n✅ Convergence atteinte à step {step}!")
            break
    
    duration = (time.time() - start_time) * 1000
    
    # Résultats
    print("\n" + "="*70)
    print("RÉSULTATS")
    print("="*70)
    
    final_states = system.get_states()
    consensus_value = sum(final_states) / len(final_states)
    
    print(f"✨ Valeur de consensus: {consensus_value:.2f}")
    print(f"📉 Variance finale: {system.variance():.4f}")
    print(f"🧊 Entités gelées: {system.frozen_ratio()*100:.0f}%")
    print(f"⏱️  Temps d'exécution: {duration:.2f}ms")
    print(f"📈 Steps effectués: {system.step_count}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()