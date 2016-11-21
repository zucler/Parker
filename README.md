# CarParker

CarParker is a web based searching engine to facilitate drivers to quickly find a parking with acceptable rates. It crawls the web to build up an up-to-date database of parking rates which is then used to serve search results to end users.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

You need to have _Docker Engine_ and _docker-compose_ installed.

### Installing

Create a new file _parker/settings.py_.

Copy the contents from _parker/settings.default.py_ into the new file.

Alternatively, on Unix/Linux systems you can simply create a symlink by running.

```
ln -s parker/settings.default.py parker/settings.py
```

Start docker containers
```
docker-compose up -d
```

## Attaching to app container

In order to run any commands and test your code, you need to be attached to the main app container. In order to do so, execute
```
docker exec -i -t carparker_parker_1 /bin/bash
```

## Downloading rates

Run the following command in order to download HTML cache for all known carparks.

```
python3 scripts/downloadParkingRatesHTML.py
```

Run the following command to process and store the cached rates.

```
python3 scripts/loadParkingRates.py
```

## Running the tests

Tests are located in *parker/tests.py*.

The main test drill function is **test_main_drill()**. If working in TDD manner, comment out every carpark test except for the one you are currently adding the support to.

To execute test run:
```
python3 manage.py test
```

## Backing up database
If any changes has been made to the data in database, they need to be backed up manually in order to not get lost. It can be done by running a **backup_db.sh** script from the main app container.


## Versioning

Used [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zucler/Parker/tags).

## Authors

- **Maxim Pak** - _Initial idea & work_ - [zucler](https://github.com/zucler)
- **Stepan Tsymbal** - _Greatest contributor_ - [ouvtk](https://github.com/ouvtk)

## License

Copyright (C) Maxim Pak - All Rights Reserved
