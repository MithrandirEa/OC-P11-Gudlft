import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


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
# Lien    : https://github.com/MithrandirEa/OC-P11-Gudlft/issues/7
@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    # Passage de la date au template
    # TODO: erase after merge
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions,
                           now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# TODO [#4] : Interdire la réservation pour les compétitions passées
# Détail : Les compétitions dont la date est antérieure à aujourd'hui ne doivent pas être réservables.
# Lien    : https://github.com/MithrandirEa/OC-P11-Gudlft/issues/4
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    # Vérification de la date de la compétition
    # TODO: erase after merge
    if datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
        flash('Cette compétition est déjà passée, vous ne pouvez pas réserver de places.')
        return render_template('welcome.html',
                               club=foundClub,
                               competitions=competitions)
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Une erreur est survenue, veuillez vérifier les informations saisies.")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


# TODO [#5] : Limiter à 12 places maximum par compétition par club
# Détail : Un club ne peut pas réserver plus de 12 places pour une même compétition.
# Lien    : https://github.com/MithrandirEa/OC-P11-Gudlft/issues/5
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > int(competition['numberOfPlaces']):
        flash('Not enough places available.')
        return render_template('booking.html',
                               club=club,
                               competition=competition)
    if placesRequired > int(club['points']):
        flash('Not enough points available.')
        return render_template('booking.html',
                               club=club,
                               competition=competition)

    competition['numberOfPlaces'] = (int(competition['numberOfPlaces'])
                                     - placesRequired)
    club['points'] = (int(club['points']) - placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions)


# TODO [#2] : Ajouter un tableau de bord des points des clubs
# Détail : Créer une route et un template permettant de consulter les points de tous les clubs.
# Lien    : https://github.com/MithrandirEa/OC-P11-Gudlft/issues/2


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
