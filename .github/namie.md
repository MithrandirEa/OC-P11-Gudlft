# Suivi des issues — Namie

> Dernière mise à jour : 2026-04-15

## Issues ouvertes

- [ ] [#2](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/2) — FEATURE: Implement Points Display Board _(fichiers : `server.py`, `templates/welcome.html`)_
  - Une secrétaire connectée devrait pouvoir voir la liste des clubs et leur solde de points actuel. Aucune route ni template n'existe pour afficher ce tableau.

- [X] [#4](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/4) — BUG: Booking places in past competitions _(fichiers : `server.py`, `templates/booking.html`)_
  - Les compétitions passées ne devraient pas être réservables. Un message d'erreur doit s'afficher ; les compétitions passées restent visibles mais sans possibilité de réservation.

- [X] [#5](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/5) — BUG: Clubs shouldn't be able to book more than 12 places per competition _(fichiers : `server.py`, `templates/booking.html`)_
  - Un club ne peut pas réserver plus de 12 places pour une même compétition. L'interface et le serveur doivent bloquer toute tentative dépassant cette limite.

- [X] [#7](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/7) — ERROR: Entering an unknown email crashes the app _(fichiers : `server.py`)_
  - Si l'email saisi ne correspond à aucun club, l'application plante (IndexError). Une erreur explicite doit être affichée à la place.

## Issues résolues

- [x] [#1](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/1) — BUG: Clubs should not be able to book more than the competition places available _(fichiers : `server.py`)_
  - La route `/purchasePlaces` vérifie désormais que le nombre de places demandées ne dépasse pas les places disponibles pour la compétition.

- [x] [#3](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/3) — BUG: Point updates are not reflected _(fichiers : `server.py`)_
  - Les points du club sont correctement déduits après une réservation (`club['points'] -= placesRequired`).

- [x] [#6](https://github.com/MithrandirEa/OC-P11-Gudlft/issues/6) — BUG: Clubs should not be able to use more than their points allowed _(fichiers : `server.py`)_
  - La route `/purchasePlaces` vérifie que le club dispose d'un solde de points suffisant avant de valider la réservation.
