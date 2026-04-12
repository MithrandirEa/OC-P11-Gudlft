# Suivi des issues — Namie

> Dernière mise à jour : 2026-04-12 (nettoyage des TODOs redondants)

> ⚠️ Les issues ci-dessous sont issues du brief officiel du projet OpenClassrooms
> ([OpenClassrooms-Student-Center/Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing)).
> Aucun outil GitHub API n'étant disponible dans cette session, les numéros d'issues
> correspondent aux éléments documentés dans le brief pédagogique du projet Gudlft.

## Issues ouvertes

- [X] [#1](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/1) — Bug : Empêcher la surréservation (overbooking) _(fichiers : `server.py`, `templates/booking.html`)_
  - La route `/purchasePlaces` ne vérifie pas que les places demandées sont disponibles. Un utilisateur peut saisir n'importe quel nombre et décrémenter les places en négatif.

- [ ] [#2](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/2) — Bug : Les points du club ne sont pas déduits lors d'une réservation _(fichiers : `server.py`)_
  - Après une réservation, `club['points']` n'est pas mis à jour. Les points doivent diminuer de 1 par place réservée.

- [ ] [#3](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/3) — Bug : Empêcher l'utilisation de plus de points que le solde disponible _(fichiers : `server.py`)_
  - Un club peut réserver autant de places qu'il le souhaite, même si son solde de points est insuffisant (règle : 1 place = 1 point).

- [ ] [#4](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/4) — Bug : Limiter à 12 places maximum par compétition par club _(fichiers : `server.py`, `templates/booking.html`)_
  - Aucune validation n'empêche un club de réserver plus de 12 places pour une même compétition.

- [ ] [#5](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/5) — Bug : Les compétitions passées sont encore réservables _(fichiers : `server.py`, `templates/welcome.html`)_
  - Les compétitions dont la date est antérieure à la date actuelle apparaissent avec un lien de réservation actif.

- [ ] [#6](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/6) — Fonctionnalité : Tableau public des points des clubs _(fichiers : `server.py`, `templates/welcome.html`)_
  - Aucune route ni template n'existe pour afficher les points de tous les clubs de manière publique (sans connexion).

- [ ] [#7](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/7) — Bug : Erreur 500 sur email invalide ou inconnu _(fichiers : `server.py`)_
  - Si l'email saisi sur la page d'accueil ne correspond à aucun club, une `IndexError` non gérée produit une erreur 500.

## Issues résolues

_(Aucune issue résolue pour l'instant dans ce suivi.)_
