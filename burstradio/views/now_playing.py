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
            'artist': 'ruairi',
            'name': 'Awful Show',
            'description': 'Not worth listening to. Don\'t bother',
        }
    )
    return {
        'playing_now': playing_now,
        'playing_next': {
            'artist': 'jcontemp',
            'name': 'Really Cool Show',
            'description': 'An analysis of all music ever.',
        },
    }
