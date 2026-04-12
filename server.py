import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


# TODO [#7] : Gérer les emails invalides / inconnus
# Détail : Une erreur 500 est levée si l'email saisi ne correspond à aucun club connu.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/7
@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions)


# TODO [#5] : Interdire la réservation pour les compétitions passées
# Détail : Les compétitions dont la date est antérieure à aujourd'hui ne doivent pas être réservables.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/5
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


# TODO [#1] : Empêcher la surréservation (overbooking)
# Détail : Vérifier que les places demandées ne dépassent pas les places disponibles dans la compétition.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/1
# TODO [#2] : Déduire les points du club lors de la réservation
# Détail : Chaque place réservée coûte 1 point ; le solde du club doit être mis à jour.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/2
# TODO [#3] : Empêcher l'utilisation de plus de points que disponibles
# Détail : Un club ne peut pas réserver plus de places que son solde de points actuel.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/3
# TODO [#4] : Limiter à 12 places maximum par compétition par club
# Détail : Un club ne peut pas réserver plus de 12 places pour une même compétition.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/4
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions)


# TODO [#6] : Ajouter une page publique affichant le tableau des points des clubs
# Détail : Créer une route et un template permettant de consulter les points de tous les clubs sans connexion.
# Lien    : https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues/6


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
