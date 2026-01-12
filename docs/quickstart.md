# Quick Start

## Installation (5 minutes)

### Option 1: Docker

```bash
git clone https://github.com/Tryboy869/nexus-stellar
cd nexus-stellar
docker build -t nexus .
docker run nexus
```

### Option 2: Local

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install dependencies
pip install numpy

# Run
python nexus_stellar.py
```

---

## Premier Programme (2 minutes)

```python
from nexus_stellar import Entity, System, Force

# Créer 10 entités
entities = [Entity(float(i)) for i in range(10)]

# Système qui converge
system = System(
    entities=entities,
    force=Force.attraction(0.5)
)

# Exécution
system.run(steps=50)

# Résultat
print(f"Variance: {system.variance()}")
```

**Résultat attendu:**
```
Variance: 0.0234
```

---

## Exemple 2: Load Balancer

```python
from nexus_stellar import Entity, System, Force, Topology

# Serveurs avec charges différentes
servers = [
    Entity(10.0, properties={'name': 'server-1'}),
    Entity(80.0, properties={'name': 'server-2'}),
    Entity(30.0, properties={'name': 'server-3'})
]

# Équilibrage automatique
system = System(
    entities=servers,
    force=Force.attraction(0.5),
    topology=Topology.full()
)

system.run_until_stable()

# Résultat
for s in servers:
    print(f"{s.properties['name']}: {s.state[0]:.1f}")
```

**Résultat:**
```
server-1: 40.0
server-2: 40.0
server-3: 40.0
```

---

## Exemple 3: Clustering

```python
from nexus_stellar import Entity, FusionEngine
import numpy as np

# 1000 vecteurs aléatoires
vectors = [np.random.random(10) for _ in range(1000)]
entities = [Entity(v) for v in vectors]

# Fusion
fusion = FusionEngine(threshold=0.5)
clusters = fusion.compress(entities)

print(f"Réduit de {len(entities)} à {len(clusters)} clusters")
```

**Résultat:**
```
Réduit de 1000 à 12 clusters
```

---

## Prochaines Étapes

- [Guide des Primitives](primitives.md)
- [Cookbook](cookbook.md)
- [API Reference](api-reference.md)