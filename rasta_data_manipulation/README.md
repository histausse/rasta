# Rasta Triturage

Triturage de donnée for the Rasta Project

## Usage

This project is managed by poetry (trying new things :-) ). To use it without poetry, you can install it as a python package in a venv:

```
git clone git@gitlab.inria.fr:jmineau/rasta_triturage.git
cd rasta_triturage
python -m venv venv
source venv/bin/activate
pip install . -e
```

The reports and information about the apk are in the prepopulated database `data.db` (TODO: add script to populate the DB)

To generate all the figures in the file `figures`:

```
rasta-triturage -d data.db -f figures
```

To display all the figures:

```
rasta-triturage -d data.db --display
```

The option `-t` allow to specify the tools to compare.

## Author

- annon
