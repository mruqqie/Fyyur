#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model): 
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime())
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete="cascade"), nullable=False, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete="cascade"), nullable=False, primary_key=True)
  
  def __repr__(self):
    return f'<{self.id},\
    {self.start_time}\
    {self.artist_id}\
    {self.venue_id}>'


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    genres = db.Column(db.String())
    website_link = db.Column(db.String())
    seeking_description = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    artists = db.relationship('Artist', secondary='show', backref=db.backref('artists', lazy=True))
    

    def __repr__(self):
      return f'<venue {self.id}\
      {self.name}\
      {self.city}\
      {self.state}\
      {self.address}\
      {self.phone}\
      {self.image_link}\
      {self.facebook_link}\
      {self.genres}\
      {self.website_link}\
      {self.seeking_description}>'




    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String())
    venues = db.relationship('Venue', secondary='show', backref=db.backref('venues', lazy=True))
    


    def __repr__(self):
      return f'<artist {self.id}\
        {self.name}\
        {self.city}\
        {self.state}\
        {self.phone}\
        {self.image_link}\
        {self.facebook_link}\
        {self.genres}\
        {self.website_link}\
        {self.seeking_description}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  venues = Venue.query.all()
  venue_by_location = Venue.query.group_by('id', 'city','state').all()
  
  for venue in venue_by_location:
    show_ven = Show.query.group_by('show.id'=='venue_id').all()
    past = 0
    upcoming = 0
    for s in show_ven:
      if (Show.start_time > datetime.now()) == True:
        upcoming += 1

    data.append({
      "state": venue.state,
      "city": venue.city,
      "venues":[{
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcoming
    }]})
      
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', '')
  venue = Venue.query.filter(Venue.name.like(f'%{search_term}%')).all()
  response = []
  con = len(venue)
  if venue:
    for ven in venue:
      show_ven = Show.query.filter(id=='venue_id').all()
      upcoming = 0
      for show in show_ven:
        if (Show.start_time > datetime.datetime.now())==True:
          upcoming += 1
  
      response.append({
       "count": con,
        "id": Venue.id,
        "name": Venue.name,
        "num_upcoming_shows": upcoming
      })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  if venue:
    # shows = Show.query.filter(venue_id).all()
    # past_shows = []
    # upcoming_shows = []

    # for show in showven:
    #   if (Show.start_time < datetime.datetime.now())==True:
    #     artist = Artist.query.get(show.artist_id)
    #     past_shows.append({
    #       "artist_id": show.artist_id,
    #       "artist_name": artist.name,
    #       "artist_image_link": artist.image_link,
    #       "start_time": show.start_time
    #     })

    #   else:
    #     (Show.start_time > datetime.datetime.now())==False
    #     artist = Artist.query.get(show.artist_id)
    #     upcoming_shows.append({
    #       "artist_id": show.artist_id,
    #       "artist_name": artist.name,
    #       "artist_image_link": artist.image_link,
    #       "start_time": show.start_time
    #     })

    data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      # "past_shows":past_shows,
      # "upcoming_shows": upcoming_shows,
      # "past_shows_count": len(past_shows),
      # "upcoming_shows_count": len(upcoming_shows)
    }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

# TODO: insert form data as a new Venue record in the db, instead
# TODO: modify data to be the data object returned from db insertion
# on successful db insert, flash success
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  website_link = request.form.get('website_link')
  seeking_talent = True if request.form.get('seeking_talent') == 'Yes' else False
  seeking_description = request.form.get('seeking_description')
  venue = Venue(name=name, city=city, state=state, address=address,
                phone=phone, genres=genres, facebook_link=facebook_link,
                image_link=image_link, website_link=website_link,
                seeking_talent=seeking_talent, seeking_description=seeking_description)
  error = False
  try:
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')

  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Venue.query.order_by(venue_id).delete()
    db.session.commit()
    flash('Delete was successful!')

  except:
    error = True
    db.session.rollback()
    flash('Delete unsuccessful!')
  
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html') #None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  artists = Artist.query.order_by('name').all
  for artist in artists():
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.like('%' + search_term + '%')).all()
  count = len(artists)
  data = []
  for artist in artists:
    shows = Show.query.filter_by(artist.id).all()
    upcoming = 0
    for show in shows:
      if (Show.start_time > datetime.datetime.now()) == True:
        upcoming += 1
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": upcoming
    })
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  # shows = Show.query.filter('id'=='artist_id').all()  
  

  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
    # "past_shows": past_shows,
    # "upcoming_shows": upcoming_shows,
    # "past_shows_count": past,
    # "upcoming_shows_count": upcoming
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  artist = Artist.query.filter_by(id=artist_id)
  artist.name = request.form.get('name')
  artist.city = request.form.get('city')
  artist.state = request.form.get('state')
  artist.phone = request.form.get('phone')
  artist.genres = request.form.get('genre')
  artist.facebook_link = request.form.get('facebook_link')
  artist.image_link = request.form.get('image_link')
  artist.website_link = request.form.get('website_link')  
  artist.seeking_venue = request.form.get('seeking_venue')
  artist.seeking_description = request.form.get('seeking_description')
  
  artists = Artist(name=name, city=city, state=state, phone=phone,
                  genre=genre, facebook_link=facebook_link, image_link=image_link,
                  website_link=website_link, seeking_venue=seeking_venue,
                  seeking_description=seeking_description)
  try:
    db.session.query(artists).update()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()


  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(id=venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  ven_up = Venue.query.get(venue_id)
  if ven_up:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.get('genres')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')
    website_link = request.form.get('website_link')
    seeking_talent = True if request.form.get('seeking_talent') == 'Yes' else False
    seeking_description = request.form.get('seeking_description')
    venues = Venue(name=name, city=city, state=state, address=address,
                phone=phone, genres=genres, facebook_link=facebook_link,
                image_link=image_link, website_link=website_link,
                seeking_talent=seeking_talent, seeking_description=seeking_description)
  error = False
  try:
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  website_link = request.form.get('website_link')
  seeking_venue = True if request.form.get('seeking_venue') == 'Yes' else False
  seeking_description = request.form.get('seeking_description')
  artist = Artist(name=name, city=city, state=state,
                phone=phone, genres=genres, facebook_link=facebook_link,
                image_link=image_link, website_link=website_link,
                seeking_venue=seeking_venue, seeking_description=seeking_description)
  error = False
  #try:
  db.session.add(artist)
  db.session.commit()
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # except:
  #   error = True
  #db.session.rollback()
  #   flash('An error occurred. Artist ' + name + ' could not be listed.')

  # finally:
  db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = []
  for s in shows:
    venue = Venue.query.filter_by(id=Show.venue_id).all()
    artist = Artist.query.filter_by(id=Show.artist_id).all()
    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')
  show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
  error = False
  try:
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
