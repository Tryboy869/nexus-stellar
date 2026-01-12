# API Reference

Documentation complète de l'API Nexus-Stellar.

---

## Entity

### Constructor

```python
Entity(state, mass=1.0, charge=0.0, velocity=None, properties=None)
```

**Paramètres:**
- `state` (float|list): État/position
- `mass` (float): Masse de l'entité
- `charge` (float): Charge électrique
- `velocity` (float|list): Vitesse initiale
- `properties` (dict): Métadonnées custom

### Attributs

- `id` (int): Identifiant unique
- `state` (np.ndarray): État actuel
- `mass` (float): Masse
- `charge` (float): Charge
- `velocity` (np.ndarray): Vitesse
- `is_frozen` (bool): État gelé
- `properties` (dict): Métadonnées

### Méthodes

#### `freeze()`
Gèle l'entité (arrête son évolution).

#### `unfreeze()`
Dégèle l'entité.

#### `distance_to(other: Entity) -> float`
Calcule distance euclidienne vers autre entité.

#### `copy() -> Entity`
Crée une copie de l'entité.

---

## Force

### Constructor

```python
Force(func: Callable)
```

### Méthodes Statiques

#### `Force.attraction(strength: float) -> Force`
Force d'attraction vers moyenne.

#### `Force.repulsion(strength: float) -> Force`
Force de répulsion.

#### `Force.gravity(G: float) -> Force`
Force gravitationnelle (F = G×m1×m2/r²).

#### `Force.spring(k: float, rest_length: float) -> Force`
Force de ressort (F = -k×distance).

#### `Force.custom(func: Callable) -> Force`
Force personnalisée.

**Signature func:**
```python
def force_func(entity1: Entity, entity2: Entity) -> np.ndarray:
    # Retourne vecteur force
    pass
```

### Méthodes

#### `compute(e1: Entity, e2: Entity)`
Calcule force entre deux entités.

---

## Topology

### Constructor

```python
Topology(func: Callable)
```

### Méthodes Statiques

#### `Topology.small_world(shortcuts: int, k: int) -> Topology`
Topologie Small-World (Watts-Strogatz).

#### `Topology.ring() -> Topology`
Topologie en anneau.

#### `Topology.full() -> Topology`
Tous connectés à tous.

#### `Topology.grid_2d(width: int, height: int) -> Topology`
Grille 2D.

#### `Topology.custom(func: Callable) -> Topology`
Topologie personnalisée.

**Signature func:**
```python
def topology_func(entity_id: int, entities: List[Entity]) -> List[int]:
    # Retourne liste IDs voisins
    pass
```

### Méthodes

#### `get_neighbors(entity_id: int, entities: List[Entity]) -> List[int]`
Retourne IDs des voisins.

---

## System

### Constructor

```python
System(
    entities: List[Entity],
    force: Force = None,
    topology: Topology = None,
    momentum: float = 0.8,
    freeze_enabled: bool = True,
    freeze_threshold: float = 0.01,
    freeze_stability_steps: int = 5
)
```

**Paramètres:**
- `entities`: Liste d'entités
- `force`: Loi de force
- `topology`: Topologie réseau
- `momentum`: Facteur d'inertie (0-1)
- `freeze_enabled`: Activer freeze
- `freeze_threshold`: Seuil stabilité
- `freeze_stability_steps`: Steps avant freeze

### Attributs

- `entities` (List[Entity]): Entités du système
- `step_count` (int): Nombre de steps
- `observers` (List[Observer]): Observers attachés
- `attractors` (List[Attractor]): Attracteurs

### Méthodes de Simulation

#### `step()`
Exécute un pas de simulation.

#### `run(steps: int)`
Exécute N pas.

#### `run_until_stable(max_steps: int, threshold: float)`
Exécute jusqu'à convergence.

### Méthodes d'Inspection

#### `variance() -> float`
Calcule variance des états.

#### `frozen_ratio() -> float`
Retourne ratio d'entités gelées (0-1).

#### `get_states() -> List[float]`
Retourne liste des états.

### Méthodes de Modification

#### `attach_observer(observer: Observer)`
Attache un observer.

#### `add_attractor(attractor: Attractor)`
Ajoute un attracteur.

---

## FusionEngine

### Constructor

```python
FusionEngine(threshold: float, method: str)
```

**Paramètres:**
- `threshold`: Distance max pour fusion
- `method`: Méthode de distance
  - `'euclidean'`: Distance euclidienne
  - `'cosine'`: Similarité cosinus
  - `'manhattan'`: Distance Manhattan

### Méthodes

#### `compress(entities: List[Entity]) -> List[Entity]`
Fusionne entités similaires.

**Retour:** Liste d'entités fusionnées (avec `mass` accumulée).

---

## Observer

### Constructor

```python
Observer(metrics: List[str], frequency: int)
```

**Paramètres:**
- `metrics`: Liste métriques à capturer
  - `'variance'`: Dispersion états
  - `'frozen_ratio'`: % gelées
  - `'energy'`: Énergie cinétique
- `frequency`: Fréquence capture (steps)

### Méthodes

#### `get_history() -> List[Dict]`
Retourne historique complet.

**Format:**
```python
[
    {'step': 0, 'variance': 150.3, 'frozen_ratio': 0.0},
    {'step': 10, 'variance': 45.2, 'frozen_ratio': 0.12},
    ...
]
```

#### `export_csv(filename: str)`
Exporte en CSV.

#### `export_json(filename: str)`
Exporte en JSON.

---

## Attractor

### Constructor

```python
Attractor(position: float, strength: float)
```

**Paramètres:**
- `position`: Position cible
- `strength`: Force d'attraction

### Attributs

- `position` (float): Position
- `strength` (float): Force

---

## Exemples Complets

### Système Simple

```python
from nexus_stellar import Entity, System, Force

entities = [Entity(float(i)) for i in range(10)]
system = System(entities, force=Force.attraction(0.5))
system.run(steps=100)
print(system.variance())
```

### Avec Observer

```python
from nexus_stellar import Observer

observer = Observer(metrics=['variance', 'frozen_ratio'])
system.attach_observer(observer)
system.run(steps=100)

history = observer.get_history()
```

### Fusion

```python
from nexus_stellar import FusionEngine

fusion = FusionEngine(threshold=1.0)
compressed = fusion.compress(entities)
print(f"Réduit à {len(compressed)} clusters")
```