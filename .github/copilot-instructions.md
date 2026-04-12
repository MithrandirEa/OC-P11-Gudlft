# GUDLFT – Project Guidelines

## Architecture

Flask POC for competition booking. No database — data lives in two JSON files:

- `clubs.json` — clubs avec `name`, `email`, `points` (valeurs **string**, pas int)
- `competitions.json` — compétitions avec `name`, `date`, `numberOfPlaces` (**string**)

Les données sont chargées en mémoire au démarrage via `loadClubs()` / `loadCompetitions()` dans `server.py`. Les mutations sur les listes `clubs` et `competitions` sont **en mémoire uniquement**, elles disparaissent au redémarrage.

## Build & Test

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
flask run          # ou : python -m flask run  (FLASK_APP=server.py par défaut)

# Lancer les tests
pytest tests/

# Couverture de code
coverage run -m pytest tests/
coverage report -m

# Tests de charge
locust -f tests/locustfile.py   # si un locustfile existe
```

## Conventions critiques

- **`points` et `numberOfPlaces` sont des strings dans les JSON.** Toujours convertir avec `int()` avant tout calcul.
- Les listes `clubs` et `competitions` sont des **globales mutables** dans `server.py`. Les tests qui modifient l'état doivent remettre les données à zéro (`setup` / `teardown`).
- Règles métier à respecter (issues ouvertes) :
  - Max **12 places** par club et par compétition (`#4`)
  - Impossible de réserver **plus de points** que le solde du club (`#3`)
  - Impossible de réserver **plus de places** que disponibles (`#1`, branche `bug/prevent-overbooking`)
  - Les **compétitions passées** ne sont pas réservables (`#5`)
  - Une réservation **déduit 1 point** par place (`#2`)

## Tests

Framework : **pytest**. Couverture : **coverage**. Tests de charge : **locust**.

Le dossier `tests/` est à peupler. Priorités :
1. Tests unitaires des règles métier dans `purchasePlaces`
2. Tests d'intégration Flask (client de test `app.test_client()`)
3. Vérification que les données JSON mutées sont correctement réinitialisées entre les tests

Pour isoler les tests, passer les listes `clubs` et `competitions` en fixtures plutôt que de dépendre des globales.

## Pièges connus

- `app.secret_key` est hardcodé (`'something_special'`) — ne pas le déplacer sans adapter les tests de session Flask.
- La route `showSummary` lève une `IndexError` si l'email est inconnu (issue `#7`, pas encore corrigée).
- La route `book` utilise `[0]` sans garde-fou → même risque d'`IndexError`.
- `htmlcov/` est généré par coverage — ne pas committer (vérifier `.gitignore`).
