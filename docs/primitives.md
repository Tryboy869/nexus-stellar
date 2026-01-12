# Guide des Primitives

Les 7 briques élémentaires de Nexus-Stellar.

---

## 1. Entity

**Concept:** Unité atomique du système (particule, serveur, agent...)

### Création

```python
from nexus_stellar import Entity

entity = Entity(
    state=10.0,           # Position/valeur
    mass=1.0,             # Masse (importance)
    charge=0.0,           # Charge électrique
    velocity=0.0,         # Vitesse initiale
    properties={'id': 1}  # Métadonnées custom
)
```

### Méthodes

```python
entity.freeze()              # Gèle l'entité
entity.unfreeze()            # Dégèle
entity.distance_to(other)    # Distance euclidienne
entity.copy()                # Clone
```

### États Multidimensionnels

```python
# 2D
entity = Entity([x, y])

# 3D
entity = Entity([x, y, z])

# N-dimensions
entity = Entity(vector)  # np.array ou list
```

---

## 2. Force

**Concept:** Définit comment les entités interagissent.

### Forces Pré-définies

```python
from nexus_stellar import Force

# Attraction vers moyenne
force = Force.attraction(strength=0.5)

# Répulsion
force = Force.repulsion(strength=0.3)

# Gravité (F = G×m1×m2/r²)
force = Force.gravity(G=1.0)

# Ressort (F = -k×distance)
force = Force.spring(k=0.8, rest_length=0.0)
```

### Force Custom

```python
def ma_force(entity1, entity2):
    distance = entity1.distance_to(entity2)
    
    if distance < 1.0:
        return -0.5  # Répulsion proche
    else:
        return 0.2   # Attraction lointaine

force = Force.custom(ma_force)
```

---

## 3. Topology

**Concept:** Définit qui interagit avec qui.

### Topologies Pré-définies

```python
from nexus_stellar import Topology

# Small-World (Watts-Strogatz)
topology = Topology.small_world(shortcuts=2)

# Anneau
topology = Topology.ring()

# Tous connectés
topology = Topology.full()

# Grille 2D
topology = Topology.grid_2d(width=10, height=10)
```

### Topology Custom

```python
def mon_reseau(entity_id, all_entities):
    # Connecte seulement entités de même type
    entity = all_entities[entity_id]
    return [
        e.id for e in all_entities
        if e.properties.get('type') == entity.properties.get('type')
    ]

topology = Topology.custom(mon_reseau)
```

---

## 4. System

**Concept:** Conteneur qui fait évoluer les entités.

### Création

```python
from nexus_stellar import System

system = System(
    entities=entities,
    force=Force.attraction(0.5),
    topology=Topology.small_world(),
    momentum=0.8,
    freeze_enabled=True,
    freeze_threshold=0.01,
    freeze_stability_steps=5
)
```

### Simulation

```python
system.step()                # 1 pas
system.run(steps=100)        # N pas
system.run_until_stable()    # Jusqu'à convergence
```

### Inspection

```python
system.variance()            # Dispersion
system.frozen_ratio()        # % gelées
system.get_states()          # Liste états
```

---

## 5. FusionEngine

**Concept:** Fusionne entités similaires (compression).

### Utilisation

```python
from nexus_stellar import FusionEngine

fusion = FusionEngine(
    threshold=1.0,      # Distance max fusion
    method='euclidean'  # Méthode distance
)

# Compression
entities = [Entity(vec) for vec in vectors]
compressed = fusion.compress(entities)
```

### Méthodes

- `'euclidean'`: Distance euclidienne
- `'cosine'`: Similarité cosinus
- `'manhattan'`: Distance Manhattan

---

## 6. Observer

**Concept:** Capture l'évolution pour analyse.

### Utilisation

```python
from nexus_stellar import Observer

observer = Observer(
    metrics=['variance', 'frozen_ratio'],
    frequency=10  # Capture toutes les 10 steps
)

system.attach_observer(observer)
system.run(steps=1000)

# Accès historique
history = observer.get_history()
# [{'step': 0, 'variance': 150}, ...]
```

### Métriques Disponibles

- `variance`: Dispersion des états
- `frozen_ratio`: % entités gelées
- `energy`: Énergie cinétique totale

---

## 7. Attractor

**Concept:** Point fixe vers lequel converger.

### Utilisation

```python
from nexus_stellar import Attractor

# Attracteur simple
attractor = Attractor(position=50.0, strength=0.3)
system.add_attractor(attractor)

# Attracteurs multiples (pour tri)
attractors = [
    Attractor(position=i, strength=0.3)
    for i in range(10)
]
system.add_attractors(attractors)
```

---

## Combinaisons

Les primitives se combinent librement:

```python
# Système complet
entities = [Entity(val) for val in data]

system = System(
    entities=entities,
    force=Force.attraction(0.5) + Force.repulsion(0.1),
    topology=Topology.small_world()
)

observer = Observer(['variance'])
system.attach_observer(observer)

system.run(steps=100)
```