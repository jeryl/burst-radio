import datetime

import transaction
from burstradio.core import db
from pyramid import httpexceptions
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import NowPlaying
from ..models import Show


def fetch_all_shows(session):
    shows = session.query(Show).order_by(Show.time.asc(), Show.id.asc()).all()
    # Split shows into two parts: show all upcoming shows first, and then shows already completed.
    current_time = datetime.datetime.now()
    next_show_index = len(shows) - 1
    for next_show_index in range(len(shows) - 1, 0, -1):
        show = shows[next_show_index]
        if show.time < current_time:
            # This is the next show
            break
    upcoming_shows = shows[next_show_index - 1:]
    completed_shows = shows[:next_show_index - 1]
    return upcoming_shows, completed_shows


def fetch_current_show(session):
    now_playing = session.query(NowPlaying).order_by(NowPlaying.time.desc(), NowPlaying.id.desc()).first()
    if now_playing is None:
        print("not playing shit")
        return None
    # nice join you got there
    return session.query(Show).filter(Show.id == now_playing.show_id).first()


def set_current_show(session, show_id):
    print("setting show to %s" % show_id)
    now_playing = NowPlaying(
        show_id=show_id,
        time=datetime.datetime.now(),
    )
    session.add(now_playing)
    # for fucks sake fuck pyramid/sqlalchemy
    session.flush()


@view_config(route_name='shows', renderer='json')
def shows(request):
    upcoming_shows, completed_shows = fetch_all_shows(request.dbsession)
    for show in (upcoming_shows + completed_shows):
        # when models pose for presentation
        show.formatted_time = '({} PT, {} CET)'.format(
            show.time.strftime("%H:%M"),
            (show.time + datetime.timedelta(hours=9)).strftime("%H:%M"),
        )
        show.artists = (
            show.artist.split("/")
            if show.artist
            else []
        )
    return {
        'upcoming_shows': [
            {
                'artist': show.artist,
                'artists': show.artists,
                'name': show.name,
                'description': show.description,
                'time': show.formatted_time,
            }
            for show in upcoming_shows
        ],
        'completed_shows': [
            {
                'artist': show.artist,
                'artists': show.artists,
                'name': show.name,
                'description': show.description,
                'time': show.formatted_time,
            }
            for show in completed_shows
        ],
    }


@view_config(route_name='current_show', renderer='json')
def current_show(request):
    set_current_show(request.dbsession, int(request.POST['show_id']))
    return HTTPFound(location=request.route_url('selecta'))


@view_config(route_name='now_playing', renderer='json')
def now_playing(request):
    current_show = fetch_current_show(request.dbsession)
    playing_now = (
        dict(artist=current_show.artist, name=current_show.name, description=current_show.description)
        if current_show
        else {
        }
    )
    return {
        'playing_now': playing_now,
        'playing_next': {
            'artist': 'lol',
            'name': 'Really Cool Show',
            'description': 'An analysis of all music ever.',
        },
    }
