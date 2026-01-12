# Cookbook

Recettes pratiques pour cas d'usage courants.

---

## 1. Load Balancer Distribué

```python
from nexus_stellar import Entity, System, Force, Topology

# Serveurs avec charges
servers = [
    Entity(load, properties={'name': f'srv-{i}'})
    for i, load in enumerate([10, 80, 30, 60, 20])
]

# Équilibrage
balancer = System(
    entities=servers,
    force=Force.attraction(0.5),
    topology=Topology.full(),
    momentum=0.8
)

balancer.run_until_stable()

# Résultat
for srv in servers:
    print(f"{srv.properties['name']}: {srv.state[0]:.1f}")
```

---

## 2. Moteur de Physique (Jeu)

```python
import random

# Particules 2D
particles = [
    Entity([random.uniform(0, 100), random.uniform(0, 100)])
    for _ in range(100)
]

# Physique avec gravité
physics = System(
    entities=particles,
    force=Force.gravity(G=1.0),
    topology=Topology.full(),
    momentum=0.9
)

# Boucle de jeu
for frame in range(1000):
    physics.step()
    
    # Render
    for p in particles:
        x, y = p.state
        draw_particle(x, y)
```

---

## 3. Tri Distribué

```python
# Liste à trier
data = [8, 3, 9, 1, 5, 2, 7, 4, 6]

# Création entités
entities = [
    Entity(float(i), properties={'value': val})
    for i, val in enumerate(data)
]

# Attracteurs (positions cibles)
attractors = [
    Attractor(position=i, strength=0.3)
    for i in range(len(data))
]

# Système de tri
sorter = System(
    entities=entities,
    attractors=attractors,
    topology=Topology.ring(),
    momentum=0.8
)

sorter.run(steps=100)

# Résultat trié
sorted_entities = sorted(entities, key=lambda e: e.state[0])
sorted_values = [e.properties['value'] for e in sorted_entities]
print(sorted_values)
```

---

## 4. Clustering de Données

```python
import numpy as np

# Dataset
vectors = [np.random.random(50) for _ in range(1000)]
entities = [Entity(vec) for vec in vectors]

# Fusion progressive
fusion = FusionEngine(threshold=0.5)
clusters = fusion.compress(entities)

print(f"Clusters: {len(clusters)}")

# Analyse
for i, cluster in enumerate(clusters):
    print(f"Cluster {i}: {cluster.mass} points")
```

---

## 5. Réseau P2P Auto-Organisé

```python
# Nœuds avec latences
nodes = [
    Entity(
        random.uniform(0, 100),
        properties={'ip': f'10.0.0.{i}'}
    )
    for i in range(50)
]

# Topologie adaptative
def proche_latence(node_id, all_nodes):
    node = all_nodes[node_id]
    distances = [
        (abs(node.state[0] - other.state[0]), other.id)
        for other in all_nodes if other.id != node_id
    ]
    distances.sort()
    return [nid for _, nid in distances[:5]]

network = System(
    entities=nodes,
    force=Force.attraction(0.3),
    topology=Topology.custom(proche_latence)
)

network.run(steps=50)
```

---

## 6. Optimisation de Fonction

```python
# Fonction à minimiser
def rastrigin(x):
    return 10 + x**2 - 10*np.cos(2*np.pi*x)

# Particules explorent espace
particles = [
    Entity(random.uniform(-5, 5))
    for _ in range(50)
]

# Force vers meilleures particules
def vers_meilleur(e1, e2):
    score1 = rastrigin(e1.state[0])
    score2 = rastrigin(e2.state[0])
    
    if score2 < score1:
        return (e2.state - e1.state) * 0.1
    return 0

optimizer = System(
    entities=particles,
    force=Force.custom(vers_meilleur),
    topology=Topology.small_world()
)

optimizer.run(steps=100)

# Meilleure solution
best = min(particles, key=lambda p: rastrigin(p.state[0]))
print(f"Optimum: x={best.state[0]:.4f}, f(x)={rastrigin(best.state[0]):.4f}")
```

---

## 7. Anti-DDoS (Fusion de Requêtes)

```python
# Requêtes légitimes + spam
requests = []

# Légitimes (signature cohérente)
for _ in range(1000):
    req = Entity(np.random.normal(5.0, 0.5, 10))
    requests.append(req)

# Spam (aléatoire)
for _ in range(10000):
    req = Entity(np.random.uniform(0, 10, 10))
    requests.append(req)

# Fusion
fusion = FusionEngine(threshold=1.0)
compressed = fusion.compress(requests)

# Légitimes fusionnent, spam reste isolé
legitimate = [c for c in compressed if c.mass > 50]
spam = [c for c in compressed if c.mass < 10]

print(f"Légitimes: {len(legitimate)}")
print(f"Spam détecté: {len(spam)}")
```

---

## 8. Système Multi-Couches

```python
# Couche physique
physical = System(
    entities=[Entity([x, y]) for x, y in positions],
    force=Force.gravity(1.0)
)

# Couche logique
logical = System(
    entities=[Entity(val) for val in values],
    force=Force.attraction(0.5)
)

# Couplage
for _ in range(100):
    physical.step()
    logical.step()
    
    # Influence mutuelle
    for p, l in zip(physical.entities, logical.entities):
        l.state[0] += 0.01 * p.state[0]
```

---

## 9. Monitoring et Analyse

```python
from nexus_stellar import Observer

# Observer custom
observer = Observer(
    metrics=['variance', 'frozen_ratio'],
    frequency=10
)

system.attach_observer(observer)
system.run(steps=1000)

# Export
observer.export_csv('simulation.csv')
observer.export_json('simulation.json')

# Analyse
import matplotlib.pyplot as plt
history = observer.get_history()
steps = [h['step'] for h in history]
variance = [h['variance'] for h in history]

plt.plot(steps, variance)
plt.xlabel('Steps')
plt.ylabel('Variance')
plt.show()
```

---

## 10. Freeze/Unfreeze Dynamique

```python
system = System(entities, force, topology)

# Exécution initiale
system.run(steps=100)

print(f"Gelées: {system.frozen_ratio()*100:.0f}%")

# Injection changement
system.inject_change(entity_id=25, new_state=100.0)

# Re-convergence locale
system.run(steps=20)

print(f"Après changement: {system.frozen_ratio()*100:.0f}%")
```