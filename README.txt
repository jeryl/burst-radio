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

- gunicorn --paste development.ini -b :8080


Where stuff lives
-----------------

Of note:
- burstradio.views.home: endpoint for our only page
- burstradio/templates/home.jinja2:  jinja template for our only page
- burstradio/static/home.js: our JS file (can add more if needed)
- burstradio/static/burstradio.css: our CSS file

Everything else:
- burstradio: everything
- burstradio.models: SQLAlchemy model definitions
- burstradio.scripts.initializedb: if you add a model to .models, you should
  also import it in this script so that the table gets created on script exec
- burstradio.static: assets including images, CSS, JS
- burstradio.templates: Jinja templates for server-side HTML rendering
- burstradio.views: code for HTTP endpoints
- burstradio.routes: enumerates all webapp routes from paths to named views
