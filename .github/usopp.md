# Plan de résolution — Usopp 🎯

> Dernière mise à jour : 2026-04-12
> Branche courante : `bug/prevent-overbooking`
> Statut global : 🔵 En cours

---

## Problèmes actifs

### 🔴 Critiques

- [ ] **[#7]** — Erreur 500 sur email invalide ou inconnu
  - Sévérité : 🔴 Critique
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → route `showSummary`
  - Problème : `[...][0]` lève une `IndexError` non gérée si l'email est inconnu → crash 500.
  - Piste recommandée : Utiliser `next((c for c in clubs if c['email'] == email), None)` + redirection avec `flash` si `None`.
  - Dépend de : rien

### 🟠 Importants

- [ ] **[#1]** — Surréservation : places demandées > places disponibles
  - Sévérité : 🟠 Important
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → `purchasePlaces`, `templates/booking.html`
  - Problème : Aucune validation — on décrémente `numberOfPlaces` sans vérifier le solde.
  - Piste recommandée : Ajouter `if placesRequired > int(competition['numberOfPlaces'])` + flash d'erreur.
  - Dépend de : rien _(peut être regroupé avec #2, #3, #4)_

- [ ] **[#2]** — Points du club non déduits après réservation
  - Sévérité : 🟠 Important
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → `purchasePlaces`
  - Problème : `club['points']` n'est jamais mis à jour après la réservation.
  - Piste recommandée : Ajouter `club['points'] = int(club['points']) - placesRequired` dans `purchasePlaces`.
  - Dépend de : rien _(regrouper avec #1, #3, #4)_

- [ ] **[#3]** — Réservation possible même sans points suffisants
  - Sévérité : 🟠 Important
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → `purchasePlaces`
  - Problème : Aucune comparaison entre `placesRequired` et `int(club['points'])`.
  - Piste recommandée : Ajouter `if placesRequired > int(club['points'])` + flash d'erreur.
  - Dépend de : rien _(regrouper avec #1, #2, #4)_

- [ ] **[#4]** — Aucune limite à 12 places par club par compétition
  - Sévérité : 🟠 Important
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` → `purchasePlaces`, `templates/booking.html`
  - Problème : Un club peut réserver 50 places d'un coup — aucune limite imposée.
  - Piste recommandée : Ajouter `if placesRequired > 12` + contrainte `max="12"` dans le formulaire.
  - Dépend de : rien _(regrouper avec #1, #2, #3)_

### 🟡 Modérés

- [ ] **[#5]** — Compétitions passées encore réservables
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
  - Dépend de : idéalement après les fixes #1–#7 pour tester le comportement corrigé.

### 🟢 Mineurs

- [ ] **[#6]** — Pas de tableau public des points des clubs
  - Sévérité : 🟢 Mineur
  - Effort : 🟢 Rapide (<1h)
  - Fichiers : `server.py` (nouvelle route `/clubs`), `templates/` (nouveau template `clubs.html`), `templates/welcome.html` (ajout d'un lien)
  - Problème : Fonctionnalité absente — aucune route ni template.
  - Piste recommandée : Ajouter `@app.route('/clubs')` retournant un template listant `clubs` ; ajouter un lien dans `welcome.html`.
  - Dépend de : rien

---

## Ordre de résolution recommandé

1. **[#7]** — Bloquant UX : crash 500 immédiat sur email inconnu. Fix isolé, rapide, sans dépendances.
2. **[#1 + #2 + #3 + #4]** — Cœur du projet : toutes dans `purchasePlaces`, à corriger en une seule passe cohérente.
3. **[#5]** — Sécurité métier : interdire les compétitions passées + mettre à jour `competitions.json` pour les tests.
4. **[Tests]** — Couvrir tous les fixes précédents avec pytest + locust.
5. **[#6]** — Feature de confort : tableau des points, faible priorité, aucune dépendance.

---

## Historique des résolutions

_(Aucune issue résolue pour l'instant dans ce suivi.)_
