#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for ,jsonify, abort, make_response
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form
from forms import *
import itertools,operator
from sqlalchemy import exc, and_
import logging

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)
logger = logging.getLogger(__name__)

# TODO: connect to a local postgresql database -- Done 23,24

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.String(300))
    talent_seek = db.Column(db.Boolean)
    talent_desc = db.Column(db.String(600))
    shows = db.relationship('Shows', backref='venue', lazy = True)

    def __init__(self, name, genres, city, state, address, phone, facebook_link):

      self.name = name
      self.genres = genres
      self.city = city
      self.state = state
      self.address = address
      self.phone = phone
      self.facebook_link = facebook_link

    def insert(self):
      db.session.add(self)
      db.session.commit()


    def update(self):
      db.session.commit()


    def delete(self):
      db.session.delete(self)
      db.session.commit()


    @property
    def past_shows(self):
      past_shows_data = list(self.shows)
      past_shows = list(filter(lambda show: (show.start_time < datetime.now()), past_shows_data))
      return [
        {
          'artist_id': show.artist.id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': show.start_time.isoformat()
        } for show in past_shows]



    @property
    def upcoming_shows(self):
      upcoming_shows_data = list(self.shows)
      upcoming_shows = list(filter(lambda show: (show.start_time > datetime.now()), upcoming_shows_data))
      return [
        {
          'artist_id': show.artist.id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': show.start_time.isoformat()
        } for show in upcoming_shows]


    @property
    def past_shows_count(self):
      """returns past show count as integer."""
      return len(self.past_shows)


    @property
    def upcoming_shows_count(self):
      """returns future show count as integer"""
      return len(self.upcoming_shows)


    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'genres': self.genres.split(', '),
        'address': self.address,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_talent': self.talent_seek,
        'seeking_description': self.talent_desc,
        'image_link': self.image_link,
        'past_shows': self.past_shows,
        'upcoming_shows': self.upcoming_shows,
        'past_shows_count': self.past_shows_count,
        'upcoming_shows_count': self.upcoming_shows_count
      }


def __repr__(self):
  return f'<Venue name={self.name}, city={self.city}, state={self.state}, address={self.address}, past_shows_count={self.past_shows_count}, upcoming_shows_count={self.upcoming_shows_count}>'


def __getitem__(self, key):
  return getattr(self, key)



    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(300))
    seeking_venue = db.Column(db.Boolean)
    seeking_venue_desc = db.Column(db.String(300))
    shows = db.relationship('Shows', backref='artist', lazy=True)

    def __init__(self, name, genres, city, state, phone, facebook_link):
      self.name = name
      self.genres = genres
      self.city = city
      self.state = state
      self.phone = phone
      self.facebook_link = facebook_link


    def insert(self):
      db.session.add(self)
      db.session.commit()


    def update(self):
      db.session.commit()


    @property
    def past_shows(self):
      past_shows_data = list(self.shows)
      past_shows = list(filter(lambda show: (show.start_time < datetime.now()), past_shows_data))
      return [
        {
          'venue_id': show.venue.id,
          'venue_name': show.venue.name,
          'venue_image_link': show.venue.image_link,
          'start_time': show.start_time.isoformat()
        } for show in past_shows]


    @property
    def upcoming_shows(self):
      upcoming_shows_data = list(self.shows)
      upcoming_shows = list(filter(lambda show: (show.start_time > datetime.now()),upcoming_shows_data))
      return [
        {
          'venue_id': show.venue.id,
          'venue_name': show.venue.name,
          'venue_image_link': show.venue.image_link,
          'start_time': show.start_time.isoformat()
        } for show in upcoming_shows]



    @property
    def past_shows_count(self):
      """int: Gets past shows count."""
      return len(self.past_shows)


    @property
    def upcoming_shows_count(self):
      """int: Gets upcoming shows count."""
      return len(self.upcoming_shows)


    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'genres': self.genres.split(', '),
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_venue': self.seeking_venue,
        'seeking_description': self.seeking_venue_desc,
        'image_link': self.image_link,
        'past_shows': self.past_shows,
        'upcoming_shows': self.upcoming_shows,
        'past_shows_count': self.past_shows_count,
        'upcoming_shows_count': self.upcoming_shows_count
      }

    def __repr__(self):
      return f'<Artist name={self.name}, city={self.city}, state={self.state}, genres={self.genres}, past_shows_count={self.past_shows_count}, upcoming_shows_count={self.upcoming_shows_count}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
  __tablename__ = 'Shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable = False)
  venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable = False)
  start_time =  db.Column(db.DateTime, nullable = False)

  def __init__(self, venue_id, artist_id, start_time):
    self.venue_id = venue_id
    self.artist_id = artist_id
    self.start_time = start_time


  def insert(self):
    db.session.add(self)
    db.session.commit()


  def update(self):
    db.session.commit()


  def format(self):
    return {
      'venue_id': self.venue.id,
      'venue_name': self.venue.name,
      'artist_id': self.artist.id,
      'artist_name': self.artist.name,
      'artist_image_link': self.artist.image_link,
      'start_time': self.start_time.isoformat()
    }


  def __repr__(self):
    return f'<Show start_time={self.start_time}, venue={self.venue}, artist={self.artist}>'



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  venue_data = Venue.query.order_by('city','state').all()
  data = [{'city': venue.city, 'state': venue.state, 'id':venue.id,'name':venue.name,'num_upcoming_shows':venue.upcoming_shows_count} for venue in venue_data]
  keyfunc = lambda v: (v['city'], v['state'])
  sorted_venues = sorted(data, key=keyfunc)
  grouped_venues = itertools.groupby(sorted_venues, key=keyfunc)

  data = [
    {
      'city': key[0],
      'state': key[1],
      'venues': list(data)
    }
    for key, data in grouped_venues]

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')

  venues_found = Venue.query.filter(
    Venue.name.match(f'%{search_term}%')).all()

  formatted_venues = [
    {
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': venue.upcoming_shows_count
    }
    for venue in venues_found]
  response = {'count': len(venues_found), 'data': list(formatted_venues)}
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()

  if venue is None:
    return abort(404)

  data = venue.format()

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)

  if form.validate_on_submit():
    error_message = 'There''s errors within the form. Please review it firstly.'
  else:
    try:
      venue_name = form.name.data
      exists = db.session.query(Venue.id).filter_by(
        name=venue_name).scalar() is not None

      if exists:
        error_message = f'Venue {venue_name} is already registered!'
      else:
        new_venue = Venue(
          name=venue_name,
          genres=', '.join(form.genres.data),
          city=form.city.data,
          state=form.state.data,
          address=form.address.data,
          phone=form.phone.data,
          facebook_link=form.facebook_link.data
        )
        new_venue.insert()

        flash(
          f'Venue {venue_name} was successfully created!', 'success')

        return redirect(url_for('show_venue', venue_id=new_venue.id))

    except exc.SQLAlchemyError as error:
      logger.exception(error, exc_info=True)
      error_message = f'An error occurred. Venue {venue_name} could not be created.'

  if error_message is not None:
    flash(error_message, 'danger')

  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  if venue is None:
    return abort(404)

  try:
    venue.delete()
    flash(f'Venue {venue.name} was successfully deleted!', 'success')

    return redirect(url_for('index'))
  except exc.IntegrityError:
    logger.exception(
      f'Error trying to delete venue {venue}', exc_info=True)
    flash(f'Venue {venue.name} can''t be deleted.', 'danger')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  Artist_data = Artist.query.order_by('id').all()
  data = [ {'id':artist.id,'name':artist.name} for artist in Artist_data]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_term', '')

  artists_found = Artist.query.filter(
    Artist.name.match(f'%{search_term}%')).all()

  formatted_artists = [{
    'id': artist.id,
    'name': artist.name,
    'num_upcoming_shows': artist.upcoming_shows_count
  }
    for artist in artists_found]
  response = {'count': len(artists_found), 'data': list(formatted_artists)}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  artist = Artist.query.filter_by(id=artist_id).first()

  if artist is None:
    return abort(404)

  data = artist.format()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_found = Artist.query.filter_by(id=artist_id).first()

  if artist_found is None:
    return abort(404)

  artist = {
    'id': artist_found.id,
    'name': artist_found.name,
    'genres': artist_found.genres.split(', '),
    'city': artist_found.city,
    'state': artist_found.state,
    'phone': artist_found.phone,
    'website': artist_found.website,
    'facebook_link': artist_found.facebook_link,
    'seeking_venue': artist_found.seeking_venue,
    'seeking_description': artist_found.seeking_venue_desc,
    'image_link': artist_found.image_link,
  }

  form = ArtistForm(formdata=None, data=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist_edited = Artist.query.filter_by(id=artist_id).first()

  if artist_edited is None:
    abort(404)

  form = ArtistForm(request.form)

  if not form.validate_on_submit():
    form.genres.data = ', '.join(form.genres.data)
    form.populate_obj(artist_edited)
    artist_edited.update()

    return redirect(url_for('show_artist', artist_id=artist_id))
  return render_template('forms/edit_artist.html', form=form, artist=artist_edited)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  venue_found = Venue.query.filter_by(id=venue_id).first()

  if venue_found is None:
    abort(404)

  venue = {
    'id': venue_found.id,
    'name': venue_found.name,
    'genres': venue_found.genres.split(', '),
    'address': venue_found.address,
    'city': venue_found.city,
    'state': venue_found.state,
    'phone': venue_found.phone,
    'website': venue_found.website,
    'facebook_link': venue_found.facebook_link,
    'image_link': venue_found.image_link
  }

  form = VenueForm(formdata=None, data=venue)

  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue_edited = Venue.query.filter_by(id=venue_id).first()

  if venue_edited is None:
    abort(404)

  form = VenueForm(request.form)

  if not form.validate_on_submit():
    form.genres.data = ', '.join(form.genres.data)
    form.populate_obj(venue_edited)
    venue_edited.update()
    return redirect(url_for('show_venue', venue_id=venue_id))
  return render_template('forms/edit_venue.html', form=form, venue=venue_edited)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)

  if form.validate_on_submit():
    error_message = 'There''s errors within the form. Please review it firstly.'
  else:
    try:
      artist_name = form.name.data
      exists = db.session.query(Artist.id).filter_by(
        name=artist_name).scalar() is not None

      if exists:
        error_message = f'Artist {artist_name} is already registered!'
      else:
        new_artist = Artist(
          name=form.name.data,
          genres=', '.join(form.genres.data),
          city=form.city.data,
          state=form.state.data,
          phone=form.phone.data,
          facebook_link=form.facebook_link.data
        )
        new_artist.insert()

        # on successful db insert, flash success
        flash(
          f'Artist {artist_name} was successfully created!', 'success')

        return redirect(url_for('show_artist', artist_id=new_artist.id))

    except exc.SQLAlchemyError as error:
      logger.exception(error, exc_info=True)
      error_message = f'An error occurred. Artist {artist_name} could not be created.'

  if error_message is not None:
    flash(error_message, 'danger')

  return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows_data = Shows.query.order_by(Shows.start_time.desc()).all()
  data = [show.format() for show in shows_data]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_show_form():
  """Instantiates the show form based on request method and populates it with the artist and venues fields choices.
  Returns
      A new instance of ShowForm.
  """
  form = ShowForm(request.form) if request.method == 'POST' else ShowForm()

  choose_option = (0, 'Select...')
  form.artist_id.choices = [choose_option]
  form.artist_id.choices += [(artist.id, artist.name)
                          for artist in Artist.query.order_by(Artist.name.asc()).all()]
  form.venue_id.choices = [choose_option]
  form.venue_id.choices += [(venue.id, venue.name)
                         for venue in Venue.query.order_by(Venue.name.asc()).all()]
  return render_template('forms/new_show.html', form=form)

def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  print(form.artist_id)
  print(form.venue_id)
  if form.validate_on_submit():
    error_message = 'There''s errors within the form. Please review it firstly.'
  else:
    try:
      artist_id = form.artist_id.data
      venue_id = form.venue_id.data
      start_time = form.start_time.data

      venue_exists = db.session.query(Venue.id).filter_by(
        id=venue_id) #.scalar() is not None
      artist_exists = db.session.query(Artist.id).filter_by(
        id=artist_id) #.scalar() is not None

      if not artist_exists:
        error_message = f'The artist with ID {artist_id} doesn\'t exists!'

      elif not venue_exists:
        error_message = f'The venue with ID {venue_id} doesn\'t exists!'

      else:
        exists = db.session.query(Shows.id). \
                   filter(and_(
          (Shows.artist_id == artist_id) &
          (Shows.venue_id == venue_id) &
          (Shows.start_time == start_time)
        )).scalar() is not None

        if exists:
          error_message = f'This show is already registered!'
        else:
          new_show = Shows(venue_id, artist_id, start_time)
          new_show.insert()

          # on successful db insert, flash success
          flash(
            f'Show at {new_show.venue.name} with {new_show.artist.name} at {new_show.start_time} was successfully created!',
            'success')

          return redirect(url_for('shows'))

    except exc.SQLAlchemyError as error:
      logger.exception(error, exc_info=True)
      error_message = f'An error occurred while show creation. Sorry, this show could not be created.'

  if error_message is not None:
    flash(error_message, 'danger')

  return render_template('forms/new_show.html', form=form)

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
