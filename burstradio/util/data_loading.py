from __future__ import absolute_import

import csv
import datetime
import simplejson as json


def filter_dict_by_keys(dictionary, keys):
    return {key: value for key, value in dictionary.iteritems() if key in keys}


def iso_to_datetime(date, time):
    date_parts = [int(x) for x in date.split('-')]
    time_parts = [int(x) for x in time.split(':')]
    return datetime.datetime(
        date_parts[0], # %Y
        date_parts[1], # %m
        date_parts[2], # %d
        time_parts[0], # %H
        time_parts[1], # %M
        0, # %s
        0, # %f
    )


def parse_program_row(row):
    # Ignore empty rows
    if not row['artist']:
        return None

    for key, value in row.items():
        row[key] = unicode(value, "utf-8")

    row['time'] = iso_to_datetime(row['date'], row['time'])
    del row['date']
    print(row)
    return row


def yield_program_csv_rows(filename):
    with open(filename) as program_csv_file:
        reader = csv.DictReader(program_csv_file)
        for row in reader:
            parsed_row = parse_program_row(row)
            if parsed_row is None:
                continue
            yield parsed_row


def yield_employees(filename):
    with open(filename) as employee_json_file:
        employee_entries = json.load(employee_json_file)
        for entry in employee_entries:
            try:
                employee = dict(
                    username=entry['meta']['username'],
                    photo_url=entry['photos'].get('ls'),
                )
            except KeyError:
                print("error for %s" % entry['meta']['username'])
                raise
            yield employee