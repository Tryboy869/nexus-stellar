# Contributing to Nexus-Stellar

Merci de votre intérêt pour contribuer à Nexus-Stellar !

---

## 🚀 Comment Contribuer

### 1. Fork et Clone

```bash
git clone https://github.com/Tryboy869/nexus-stellar
cd nexus-stellar
```

### 2. Créer une Branche

```bash
git checkout -b feature/ma-nouvelle-feature
```

### 3. Faire vos Modifications

- Suivez le style de code existant
- Ajoutez des tests si nécessaire
- Documentez les nouvelles fonctionnalités

### 4. Tester

```bash
python tests/test_entity.py
python tests/test_system.py
python tests/test_fusion.py
```

### 5. Commit et Push

```bash
git add .
git commit -m "feat: description de la feature"
git push origin feature/ma-nouvelle-feature
```

### 6. Pull Request

Créez une PR sur GitHub avec:
- Description claire des changements
- Cas d'usage
- Tests ajoutés

---

## 📝 Guidelines

### Style de Code

- Python: PEP 8
- Docstrings pour toutes les fonctions publiques
- Type hints quand possible

### Commits

Format: `type: description`

Types:
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactoring

### Tests

Tous les nouveaux codes doivent être testés:

```python
def test_ma_feature():
    """Test description"""
    # Test code
    assert result == expected
    print("✅ test_ma_feature")
```

---

## 🐛 Rapporter des Bugs

Créez une issue avec:
- Description du bug
- Steps pour reproduire
- Comportement attendu vs actuel
- Version Python/OS

---

## 💡 Proposer des Features

Créez une issue avec:
- Description de la feature
- Cas d'usage
- Proposition d'implémentation

---

## 📧 Contact

**Daouda Abdoul Anzize**  
nexusstudio100@gmail.com

---

## ⚖️ License

En contribuant, vous acceptez que vos contributions soient sous licence MIT.