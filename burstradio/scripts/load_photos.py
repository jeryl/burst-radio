import argparse
import csv
import datetime
import os
import simplejson as json
import urllib

from burstradio.core import db
from burstradio.models import Show
from burstradio.util import data_loading


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load photos for show hosts into burstradio/static/photos."
    )
    parser.add_argument(
        'program_csv',
        type=str,
        help="Path to program CSV file."
    )
    parser.add_argument(
        'employees_file',
        type=str,
        help="Path to employees.json file from https://yelpfacetiles.appspot.com"
    )
    parser.add_argument(
        'photos_dir',
        type=str,
        help="Path to photos directory (e.g. burstradio/static/photos)"
    )
    parser.add_argument('-v', '--verbose', action='store_true', help="Talk a lot.")
    args = parser.parse_args()
    assert args.program_csv
    assert args.employees_file
    assert args.photos_dir

    assert os.path.isdir(args.photos_dir)

    return args


def run():
    args = parse_args()

    artists = set([
        row['artist']
        for row in data_loading.yield_program_csv_rows(args.program_csv)
    ])
    print(artists)

    artist_info_list = [
        employee
        for employee in data_loading.yield_employees(args.employees_file)
        if employee['username'] in artists
    ]

    for artist_info in artist_info_list:
        if artist_info['photo_url'] is None:
            print("%s: no photo URL" % artist_info['username'])
            continue
        target_filename = '%s/%s.jpg' % (args.photos_dir, artist_info['username'])
        urllib.urlretrieve(artist_info['photo_url'], target_filename)
        print("%s: writing %s" % (artist_info['username'], target_filename))



if __name__ == '__main__':
    run()
