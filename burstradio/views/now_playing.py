from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Show


@view_config(route_name='now_playing', renderer='json')
def now_playing(request):
    return {
        'playing_now': {
            'name': 'ruairi',
            'title': 'Awful Show',
            'description': 'Not worth listening to. Don\'t bother',
        },
        'playing_next': {
            'name': 'jcontemp',
            'title': 'Really Cool Show',
            'description': 'An analysis of all music ever.',
        },
    }
