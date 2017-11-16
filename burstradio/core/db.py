import contextlib
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )


from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)


engine = None
session_factory = None


def initialize_db(config_uri):
    # jank AF
    global engine
    global session_factory

    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = get_engine(settings)

    session_factory = get_session_factory(engine)


@contextlib.contextmanager
def transaction_session():
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        yield dbsession
