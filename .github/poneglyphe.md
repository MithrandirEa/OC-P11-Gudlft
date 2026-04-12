# Ponéglyphe — Synthèse du projet Güdlft Registration

> **Dépôt** : `OpenClassrooms-Student-Center/Python_Testing`
> **Branche courante** : `bug/prevent-overbooking`
> **Date de rédaction** : 12 avril 2026

---

## 1. Rôle et objectif

**Güdlft Registration** est un **proof of concept (POC)** d'une plateforme légère de réservation de places pour des compétitions sportives, destinée à des clubs d'haltérophilie.

Le projet permet à un secrétaire de club de :
- S'authentifier par email
- Consulter les compétitions disponibles et leurs places restantes
- Réserver des places pour son club dans une compétition
- Se déconnecter

L'objectif est de garder l'application la plus simple possible et d'itérer à partir des retours utilisateurs.

---

## 2. Architecture technique

### Stack

| Composant | Technologie |
|-----------|-------------|
| Backend | **Python 3.x** + **Flask** |
| Templates | **Jinja2** (intégré à Flask) |
| Base de données | **Fichiers JSON** (pas de BDD relationnelle) |
| Tests | Dossier `tests/` prévu (actuellement vide) |
| Couverture | Module `coverage` (rapport HTML dans `htmlcov/`) |

### Structure des fichiers

```
.
├── server.py              # Point d'entrée — routes Flask et logique métier
├── clubs.json             # Données des clubs (nom, email, points)
├── competitions.json      # Données des compétitions (nom, date, places)
├── requirements.txt       # Dépendances Python
├── README.md              # Documentation d'origine
├── templates/
│   ├── index.html         # Page de connexion (saisie email)
│   ├── welcome.html       # Tableau de bord — liste des compétitions
│   └── booking.html       # Formulaire de réservation de places
├── tests/                 # Répertoire de tests (vide)
├── htmlcov/               # Rapport de couverture de code
└── .github/
    ├── agents/
    │   └── namie.agent.md # Agent de suivi des issues
    └── poneglyphe.md      # Ce document
```

### Modèle de données (JSON)

**`clubs.json`** — 3 clubs :

| Club | Email | Points |
|------|-------|--------|
| Simply Lift | john@simplylift.co | 13 |
| Iron Temple | admin@irontemple.com | 4 |
| She Lifts | kate@shelifts.co.uk | 12 |

**`competitions.json`** — 2 compétitions :

| Compétition | Date | Places |
|-------------|------|--------|
| Spring Festival | 2020-03-27 10:00 | 25 |
| Fall Classic | 2020-10-22 13:30 | 13 |

> ⚠️ Les deux compétitions ont des dates **dans le passé** (2020), ce qui est lié à l'issue #5.

---

## 3. Flux principal

```
[Utilisateur] → GET /
                  ↓
            index.html (saisie email)
                  ↓
          POST /showSummary (email)
                  ↓
        Recherche du club par email dans clubs.json
                  ↓
            welcome.html (liste des compétitions + points du club)
                  ↓
        GET /book/<competition>/<club>
                  ↓
            booking.html (formulaire : nombre de places)
                  ↓
        POST /purchasePlaces (club, competition, places)
                  ↓
        Déduction des places de la compétition (en mémoire)
                  ↓
            welcome.html (message de confirmation)
                  ↓
        GET /logout → redirection vers /
```

### Détails importants du flux

1. **Authentification** : simple recherche par email dans la liste en mémoire — pas de mot de passe, pas de session persistante.
2. **Données en mémoire** : les JSON sont chargés au démarrage (`loadClubs()`, `loadCompetitions()`). Les modifications (déduction de places) ne sont **pas persistées** sur disque.
3. **Clé secrète Flask** : codée en dur (`'something_special'`), adaptée uniquement pour un POC.

---

## 4. Routes de l'application

| Route | Méthode | Fonction | Description |
|-------|---------|----------|-------------|
| `/` | GET | `index()` | Page d'accueil — formulaire de connexion |
| `/showSummary` | POST | `showSummary()` | Authentification par email, affiche le tableau de bord |
| `/book/<competition>/<club>` | GET | `book()` | Affiche le formulaire de réservation |
| `/purchasePlaces` | POST | `purchasePlaces()` | Traite la réservation de places |
| `/logout` | GET | `logout()` | Déconnexion — redirige vers `/` |

---

## 5. Issues connues et TODOs

Le projet comporte **7 issues** identifiées, toutes documentées par des commentaires TODO dans le code :

| # | Issue | Fichier(s) concerné(s) | Criticité |
|---|-------|------------------------|-----------|
| 1 | Empêcher la surréservation (overbooking) | `server.py`, `booking.html` | 🔴 Haute |
| 2 | Déduire les points du club lors de la réservation | `server.py` | 🔴 Haute |
| 3 | Empêcher l'utilisation de plus de points que disponibles | `server.py` | 🔴 Haute |
| 4 | Limiter à 12 places max par compétition par club | `server.py`, `booking.html` | 🟠 Moyenne |
| 5 | Interdire la réservation pour les compétitions passées | `server.py`, `welcome.html` | 🟠 Moyenne |
| 6 | Ajouter un tableau public des points des clubs | `server.py`, `welcome.html` | 🟡 Basse |
| 7 | Gérer les emails invalides / inconnus | `server.py` | 🔴 Haute |

### Analyse des risques par issue

- **Issues #1, #2, #3** (fonction `purchasePlaces`) : la route actuelle ne fait **aucune validation** — elle soustrait aveuglément les places demandées sans vérifier les limites. C'est le cœur du bug sur la branche courante.
- **Issue #5** : les compétitions passées restent réservables car aucune comparaison de date n'est effectuée.
- **Issue #7** : si l'email n'existe pas, `[0]` sur une liste vide provoque un `IndexError` → erreur 500.

---

## 6. Points d'attention

### Sécurité
- **Clé secrète en dur** : `app.secret_key = 'something_special'` — à externaliser via variable d'environnement en production.
- **Pas de validation d'entrée** : les formulaires ne valident ni le format ni les bornes des valeurs saisies.
- **Pas de protection CSRF** explicite (Flask-WTF non utilisé, mais Flask gère les sessions signées).

### Robustesse
- **Aucune gestion d'erreur** : les recherches par `[0]` sur des listes filtrées lèvent `IndexError` si aucun résultat.
- **Données non persistées** : les modifications en mémoire sont perdues au redémarrage du serveur.
- **Types JSON** : les `points` et `numberOfPlaces` sont des **chaînes** dans le JSON, nécessitant des conversions `int()` à chaque usage.

### Tests
- Le répertoire `tests/` est **vide** — aucun test unitaire ou fonctionnel n'existe encore.
- Un rapport `htmlcov/` est présent, suggérant qu'une couverture a été lancée, mais sans tests associés.

### Dettes techniques
- Toute la logique est dans un seul fichier `server.py` (pas de séparation modèle/vue/contrôleur).
- Les templates HTML sont minimalistes (pas de `<head>` complet, pas de CSS).

---

## 7. Glossaire

| Terme | Définition |
|-------|------------|
| **Club** | Organisation sportive disposant de points pour réserver des places en compétition |
| **Points** | Monnaie virtuelle du club — chaque place réservée coûte des points |
| **Compétition** | Événement avec un nombre limité de places réservables par les clubs |
| **POC** | Proof of Concept — version minimale pour valider le concept |
| **Güdlft** | Nom de la plateforme de gestion des compétitions d'haltérophilie |
| **Overbooking** | Réservation de plus de places que disponibles — bug principal du projet |
