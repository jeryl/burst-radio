import argparse

from burstradio.core import db
from burstradio.models import Show
from burstradio.util import data_loading


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load program shows into database."
    )
    parser.add_argument(
        'program_csv',
        type=str,
        help="Name of program CSV file."
    )
    parser.add_argument(
        'config_file',
        type=str,
        help="Name of config file (e.g. development.ini)"
    )
    parser.add_argument('-v', '--verbose', action='store_true', help="Talk a lot.")
    args = parser.parse_args()
    assert args.program_csv
    assert args.config_file
    return args


def create_show(row):
    with db.transaction_session() as session:
        show = Show(
            time=row['time'],
            artist=row['artist'],
            name=row['name'],
            description=row['description'],
        )
        session.add(show)


def dump_database():
    with db.transaction_session() as session:
        shows = session.query(Show).all()
        for show in shows:
            print(dict(
                time=show.time,
                artist=show.artist,
                name=show.name,
                description=show.description,
            ))


def run():
    args = parse_args()
    db.initialize_db(args.config_file)

    for row in data_loading.yield_program_csv_rows(args.program_csv):
        create_show(row)

    dump_database()


if __name__ == '__main__':
    run()
