# taipan-library

# Installation Instructions
```bash
$ mkvirtualenv -p $(which python3) taipan
$ cdvirtualenv
$ mkdir src && cd src
$ git clone git@github.com:dice-group/TAIPAN.git && cd TAIPAN
$ pip install -e .
```

# Dev
```
make dev
make test
```

# Subject column identification
For subject column identification use scidentifier script as follows:
```
scidentifier table.csv
```
