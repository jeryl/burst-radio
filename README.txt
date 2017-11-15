burstradio README
==================

This webapp uses the default SQLAlchemy scaffold for Pyramid 1.9, which means
SQLAlchemy 1.2 on a local SQLite file.  YOLO


Getting Started
---------------

- cd <directory containing this file>

- virtualenv venv

- source venv/bin/activate

- pip install --upgrade pip setuptools

- pip install -r requirements.txt

- python setup.py develop


Creating SQLite tables
----------------------

- initialize_burstradio_db development.ini


Running the server for development
----------------------------------

- pserve development.ini


Running the server for realz
----------------------------

- gunicorn --paste development.ini -b :80


Where stuff lives
-----------------

- burstradio: everything
- burstradio.models: SQLAlchemy model definitions
- burstradio.scripts: initialization / command line scripts
- burstradio.static: assets including images, CSS, JS
- burstradio.templates: Jinja templates for server-side HTML rendering
- burstradio.views: code for HTTP endpoints
- burstradio.routes.py: enumerates all webapp routes from paths to named views