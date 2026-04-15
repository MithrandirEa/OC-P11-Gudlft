# Plan de résolution — Usopp 🎯

> Dernière mise à jour : 2026-04-15
> Branche courante : `development`
> Statut global : 🔵 En cours

---

## Problèmes actifs

### 🔴 Critiques

- [ ] **[#7](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/7)** — Erreur 500 sur email invalide ou inconnu
  - Sévérité : 🔴 Critique
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → route `showSummary`
  - Problème : `[...][0]` lève une `IndexError` non gérée si l'email est inconnu → crash 500.
  - Piste recommandée : Utiliser `next((c for c in clubs if c['email'] == email), None)` + redirection avec `flash` si `None`.
  - Dépend de : rien

### 🟠 Importants

- [ ] **[#5](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/5)** — Aucune limite à 12 places par club par compétition
  - Sévérité : 🟠 Important
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → `purchasePlaces`, `templates/booking.html`
  - Problème : Un club peut réserver 50 places d'un coup — aucune limite imposée.
  - Piste recommandée : Ajouter `if placesRequired > 12` + contrainte `max="12"` dans le formulaire.
  - Dépend de : rien

### 🟡 Modérés

- [ ] **[#4](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/4)** — Compétitions passées encore réservables
  - Sévérité : 🟡 Modéré
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → `book`, `templates/welcome.html`
  - Problème : Aucune comparaison de `competition['date']` avec la date actuelle.
  - ⚠️ **Attention** : les deux compétitions en JSON datent de 2020 → toutes passées. Il faudra ajouter une compétition future dans `competitions.json` pour les tests manuels.
  - Piste recommandée : Comparer `datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") < datetime.now()` dans `book` et dans le template Jinja2.
  - Dépend de : rien

- [ ] **[Tests]** — Dossier `tests/` entièrement vide
  - Sévérité : 🟡 Modéré
  - Effort : 🟡 Moyen (1-4h)
  - Fichiers : `tests/` (à créer), `server.py`
  - Problème : Aucun test unitaire ni d'intégration n'existe. Impossible de valider les fixes sans régression.
  - Piste recommandée : Créer `tests/conftest.py` (fixtures clubs/competitions isolées), `tests/test_server.py` (tests unitaires des règles métier) et `tests/test_integration.py` (client Flask).
  - Dépend de : idéalement après les fixes #4, #5, #7 pour tester le comportement corrigé.

### 🟢 Mineurs

- [ ] **[#2](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/2)** — Pas de tableau des points des clubs
  - Sévérité : 🟢 Mineur
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` (nouvelle route `/clubs`), `templates/` (nouveau template `clubs.html`), `templates/welcome.html` (ajout d'un lien)
  - Problème : Fonctionnalité absente — aucune route ni template.
  - Piste recommandée : Ajouter `@app.route('/clubs')` retournant un template listant `clubs` ; ajouter un lien dans `welcome.html`.
  - Dépend de : rien

---

## Ordre de résolution recommandé

1. **[#7]** — Bloquant UX : crash 500 immédiat sur email inconnu. Fix isolé, rapide, sans dépendances.
2. **[#5]** — Sécurité métier : limiter à 12 places par club et par compétition.
3. **[#4]** — Sécurité métier : interdire les compétitions passées + mettre à jour `competitions.json` pour les tests.
4. **[Tests]** — Couvrir tous les fixes avec pytest + locust.
5. **[#2]** — Feature de confort : tableau des points, faible priorité, aucune dépendance.

---

## Historique des résolutions

- [x] **[#1](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/1)** — Surréservation : places demandées > places disponibles — Résolu (vérification `placesRequired > int(competition['numberOfPlaces'])` ajoutée dans `purchasePlaces`).
- [x] **[#3](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/3)** — Points du club non déduits après réservation — Résolu (`club['points'] = int(club['points']) - placesRequired` ajouté dans `purchasePlaces`).
- [x] **[#6](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/6)** — Réservation possible même sans points suffisants — Résolu (vérification `placesRequired > int(club['points'])` ajoutée dans `purchasePlaces`).
