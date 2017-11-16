import argparse
import csv
import datetime

from burstradio.core import db
from burstradio.models import Show


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
    return args



def filter_dict_by_keys(dictionary, keys):
    return {key: value for key, value in dictionary.iteritems() if key in keys}


def iso_to_datetime(val):
    print(val)
    return datetime.datetime(
        int(val[0:4]), # %Y
        int(val[5:7]), # %m
        int(val[8:10]), # %d
        int(val[11:13]), # %H
        int(val[14:16]), # %M
        0, # %s
        0, # %f
    )


def load_row(row):
    for key, value in row.items():
        row[key] = unicode(value, "utf-8")

    row['time'] = "%sT%s" % (row['date'], row['time'])
    del row['date']
    row['time'] = iso_to_datetime(row['time'])

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

    with open(args.program_csv) as program_csv_file:
        reader = csv.DictReader(program_csv_file)
        for row in reader:
            load_row(row)

    dump_database()



if __name__ == '__main__':
    run()
