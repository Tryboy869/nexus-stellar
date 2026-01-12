"""
Exemple: Moteur de Physique pour Jeu
Démontre la simulation de particules 2D avec forces émergentes
"""

import sys
sys.path.append('..')

from nexus_stellar import Entity, System, Force, Topology
import random
import time
import numpy as np

def main():
    print("="*70)
    print("NEXUS-STELLAR: Moteur de Physique 2D")
    print("="*70 + "\n")
    
    # Génération particules
    print("⚛️  Génération de 50 particules...")
    
    particles = []
    for i in range(50):
        x = random.uniform(10, 90)
        y = random.uniform(10, 90)
        
        particle = Entity(
            state=[x, y],
            mass=random.uniform(0.5, 2.0),
            velocity=[random.uniform(-1, 1), random.uniform(-1, 1)],
            properties={'id': i, 'color': random.choice(['red', 'blue', 'green'])}
        )
        particles.append(particle)
    
    print(f"   {len(particles)} particules créées\n")
    
    # Force physique custom
    def physics_force(e1, e2):
        """Force combinée: gravité faible + répulsion forte si proche"""
        dx = e2.state[0] - e1.state[0]
        dy = e2.state[1] - e1.state[1]
        r = np.sqrt(dx**2 + dy**2)
        
        if r < 0.1:
            r = 0.1
        
        # Répulsion forte si distance < 5
        if r < 5.0:
            force_mag = -5.0 / r
        else:
            # Gravité faible sinon
            force_mag = e1.mass * e2.mass / (r**2) * 0.1
        
        fx = force_mag * dx / r
        fy = force_mag * dy / r
        
        return np.array([fx, fy])
    
    # Système physique
    print("🎮 Création moteur physique...")
    physics = System(
        entities=particles,
        force=Force.custom(physics_force),
        topology=Topology.full(),
        momentum=0.9,
        freeze_enabled=False
    )
    
    # Simulation
    print("🚀 Démarrage simulation (100 frames)...\n")
    start_time = time.time()
    
    frame_times = []
    
    for frame in range(100):
        frame_start = time.time()
        physics.step()
        frame_time = (time.time() - frame_start) * 1000
        frame_times.append(frame_time)
        
        if frame % 20 == 0:
            print(f"   Frame {frame:3d} | Temps frame: {frame_time:.2f}ms")
    
    total_duration = (time.time() - start_time) * 1000
    
    # Résultats
    print("\n" + "="*70)
    print("RÉSULTATS")
    print("="*70)
    
    avg_frame_time = sum(frame_times) / len(frame_times)
    fps = 1000 / avg_frame_time if avg_frame_time > 0 else 0
    
    print(f"⏱️  Temps total: {total_duration:.2f}ms")
    print(f"📊 Temps moyen/frame: {avg_frame_time:.2f}ms")
    print(f"🎬 FPS théorique: {fps:.1f}")
    print(f"\n📍 Positions finales (5 premières particules):")
    
    for p in particles[:5]:
        x, y = p.state
        print(f"   Particule {p.properties['id']:2d}: ({x:6.2f}, {y:6.2f}) | "
              f"Couleur: {p.properties['color']}")
    
    print("\n💡 Note: Dans un vrai jeu, chaque frame appellerait physics.step()")
    print("   puis rendrait les particules aux positions mises à jour.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()