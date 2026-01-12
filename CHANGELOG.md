# Changelog

Toutes les modifications notables de Nexus-Stellar sont documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] - 2026-01-12

### Added
- 🌟 Release initiale
- ⚛️ 7 primitives fondamentales (Entity, Force, Topology, System, FusionEngine, Observer, Attractor)
- 🦀 Moteur Rust avec parallélisation Rayon (calculs multi-cœurs)
- ⚡ Moteur C++ avec optimisation marquage (évite O(N²))
- 🐳 Support Docker pour portabilité universelle
- 📚 Documentation complète (quickstart, primitives, cookbook, API)
- 🧪 Suite de tests (Entity, System, Fusion)
- 📦 5 exemples fonctionnels (consensus, sorting, clustering, load_balancer, game_physics)
- 🧊 Freeze mechanism (économie 100% en régime stable)
- 🌐 Topologies validées (Small-World, Ring, Full, Grid)
- 💾 Cache intelligent (pas de recompilation inutile)

### Optimizations
- Parallélisation Rust avec Rayon pour calculs force
- Marquage au lieu d'erase en C++ (fusion O(N) vs O(N²))
- Fallback rustc si Cargo non disponible

### Known Limitations
- Version alpha (API peut changer)
- Rust Rayon nécessite Cargo (fallback disponible)
- Tests nécessitent compilation Rust/C++ manuelle

---

## [Unreleased]

### Planned for v0.2.0
- 🔄 Support WebAssembly (run in browser)
- 📊 Visualisation temps réel (matplotlib integration)
- 🎨 API haut niveau (presets pour cas courants)
- 🚀 Benchmarks comparatifs vs algorithmes classiques
- 📱 Support mobile (iOS/Android via Kivy)

### Planned for v1.0.0
- ✅ API stable
- 📦 PyPI publication
- 🌍 Support multi-langages (Go, Zig, Julia)
- 🧠 Primitives avancées (Memory, Learning, Evolution)
- 🏆 Production-ready

---

## Contact

**Daouda Abdoul Anzize**  
Nexus Studio  
nexusstudio100@gmail.com  
GitHub: [@Tryboy869](https://github.com/Tryboy869)