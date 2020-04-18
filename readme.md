# Energy Data App

## Installation
1. Create conda environment: `conda env create -n energy_data python=3.8`
2. `conda activate energy_data`
3. Setup [poetry](https://python-poetry.org)
4. `poetry install`
5. Initialize the database:
```
CREATE USER postgres SUPERUSER;
CREATE USER energydbuser WITH PASSWORD '1234';
CREATE DATABASE energydb WITH OWNER = postgres;
GRANT ALL PRIVILEGES ON DATABASE energydb to energydbuser;
ALTER ROLE energydbuser SET client_encoding TO 'utf8';
ALTER ROLE energydbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE energydbuser SET timezone TO 'UTC';
ALTER USER energydbuser CREATEDB;
exit;
```
