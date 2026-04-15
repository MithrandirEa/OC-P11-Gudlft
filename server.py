import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

MAX_BOOKABLE_PLACES = 12

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


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = next((c for c in clubs if c['email'] == request.form['email']), None)
    if club is None:
        flash("Désolé, cet email n'a pas été trouvé.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions,
                           now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

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


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > MAX_BOOKABLE_PLACES:
        flash(f'Vous ne pouvez pas réserver plus de {MAX_BOOKABLE_PLACES} places pour une même compétition.')
        return render_template('booking.html',
                               club=club,
                               competition=competition)
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

@app.route('/clubs')
def clubs_board():
    return render_template('clubs.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
