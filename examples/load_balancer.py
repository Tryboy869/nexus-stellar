"""
Exemple: Load Balancer Distribué
Démontre l'équilibrage automatique de charge entre serveurs
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, System, Force, Topology, Observer
import random
import time

def main():
    print("="*70)
    print("NEXUS-STELLAR: Load Balancer Distribué")
    print("="*70 + "\n")
    
    # Création serveurs avec charges déséquilibrées
    print("🖥️  Initialisation de 10 serveurs...")
    
    initial_loads = [10, 80, 30, 90, 20, 85, 15, 75, 25, 95]
    
    servers = [
        Entity(
            state=float(load),
            properties={
                'name': f'server-{i:02d}',
                'ip': f'10.0.0.{i+1}',
                'max_capacity': 100
            }
        )
        for i, load in enumerate(initial_loads)
    ]
    
    print("   État initial:")
    for srv in servers:
        load = srv.state[0]
        bar = '█' * int(load/10) + '░' * (10 - int(load/10))
        print(f"   {srv.properties['name']} ({srv.properties['ip']}): [{bar}] {load:.0f}%")
    
    print(f"\n   Déséquilibre: {max(initial_loads) - min(initial_loads):.0f}%\n")
    
    # Système d'équilibrage
    print("⚖️  Création système d'équilibrage...")
    balancer = System(
        entities=servers,
        force=Force.attraction(strength=0.5),
        topology=Topology.full(),
        momentum=0.8,
        freeze_enabled=True
    )
    
    # Observer
    observer = Observer(metrics=['variance'], frequency=5)
    balancer.attach_observer(observer)
    
    # Équilibrage
    print("🚀 Démarrage équilibrage...\n")
    start_time = time.time()
    
    for step in range(100):
        balancer.step()
        
        if step % 20 == 0:
            var = balancer.variance()
            print(f"   Step {step:3d} | Variance: {var:8.2f}")
        
        if balancer.variance() < 1.0:
            print(f"\n✅ Équilibre atteint à step {step}!")
            break
    
    duration = (time.time() - start_time) * 1000
    
    # Résultats
    print("\n" + "="*70)
    print("RÉSULTATS")
    print("="*70 + "\n")
    
    print("   État final:")
    final_loads = [s.state[0] for s in servers]
    
    for srv in servers:
        load = srv.state[0]
        bar = '█' * int(load/10) + '░' * (10 - int(load/10))
        print(f"   {srv.properties['name']} ({srv.properties['ip']}): [{bar}] {load:.0f}%")
    
    print(f"\n📊 Statistiques:")
    print(f"   Charge moyenne: {sum(final_loads)/len(final_loads):.1f}%")
    print(f"   Charge min: {min(final_loads):.1f}%")
    print(f"   Charge max: {max(final_loads):.1f}%")
    print(f"   Déséquilibre: {max(final_loads) - min(final_loads):.1f}%")
    print(f"\n⏱️  Temps: {duration:.2f}ms")
    print(f"📈 Steps: {balancer.step_count}")
    print(f"🧊 Gelées: {balancer.frozen_ratio()*100:.0f}%")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()