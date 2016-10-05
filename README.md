# CarParker

CarParker is a web based searching engine to facilitate drivers to quickly find a parking with acceptable rates. It crawls the web to build up an up-to-date database of parking rates which is then used to serve search results to end users.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

Set up a python virtualenv and install packages listed in *vitualenv_packages.txt*

To make pip install all packages:

```
pip install -r path/to/virtualenv_packages.txt
```

### Installing

Update config by making changes in *parker/settings.py* file.

```
#Set your DB connection details below:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'parker',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': 'root',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
    }
}
```

Run the following command in order to download HTML cache for all known carparks.

```
python scripts/downloadParkingRatesHTML.py
```

Run the following command to process and store the cached rates.

```
python scripts/loadParkingRates.py
```

## Running the tests

Tests are located in *parker/tests.py*.

The main test drill function is **test_main_drill()**. If working in TDD manner, comment out every carpark test except for the one you are currently adding the support to.

To execute test run:
```
./manage.py test
```

## Versioning

Used [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zucler/Parker/tags).

## Authors

- **Maxim Pak** - _Initial idea & work_ - [zucler](https://github.com/zucler)
- **Stepan Tsymbal** - _Greatest contributor_ - [ouvtk](https://github.com/ouvtk)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Copyright (C) Maxim Pak - All Rights Reserved
