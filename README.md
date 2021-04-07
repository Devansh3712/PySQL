<p align = "center">
  <a href = "https://github.com/Devansh3712/PySQL"><img src = "https://user-images.githubusercontent.com/58616444/113156144-57560f80-9257-11eb-85a1-1b834c072454.png"></a>
</p>

<h1 align = "center"> PySQL </h1>
<p align = "center"><i> GUI & Python wrapper for making MySQL queries easier </i></p>

<p align = "center">
  <a href = "https://www.python.org"><img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href = "https://www.mysql.com/"><img src="https://camo.githubusercontent.com/4524c09f8c821218b3c602e3e5a222ce00c290c2f87e264b40f398a6b486bd91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6d7973716c2d2532333030303030662e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6d7973716c266c6f676f436f6c6f723d7768697465"/></a>
  <a href = "./LICENSE"><img src = "https://img.shields.io/github/license/Devansh3712/PySQL?style=for-the-badge"></a>
  <a href = "https://pypi.org/project/pysql-cli/"><img src = "https://img.shields.io/badge/PyPi-1.0.7-blue?style=for-the-badge&logo=appveyor"></a>
</p>

---

## Installation

- Clone the repository to your local machine

```console
git clone https://github.com/Devansh3712/PySQL.git
```

- Installation pre-requisites

  - ``MySQL server``
  - ``Python virtualenv``

- PyPi package

> Windows

```console
pip install pysql-cli
```

> Linux / MacOS

```console
pip3 install pysql-cli
```

- Automatic Setup

Open the ``PySQL`` directory, run the setup file & activate the ``virtual environment``

> Windows

```console
setup.cmd
venv\Scripts\activate.bat
```

> Linux / MacOS

```console
chmod +x ./setup.sh
. setup.sh
source venv/bin/activate
```

- Manual Setup

Open the ``PySQL`` directory

> using requirements.txt

```console
pip install -r requirements.txt
```

> using poetry

```console
poetry install
```

## Usage

- Using the pip package

  - ``pysql``: Basic PySQL CLI
  - ``cpysql``: Colored PySQL CLI

```console
pysql
cpysql
```

- Using the Python command-line wrapper `.py file`

  - ``main.py``: Basic PySQL CLI
  - ``main_c.py``: Colored PySQL CLI

> Windows

```console
python pysql/main.py
python pysql/main_c.py
```

> Linux

```console
python3 pysql/main.py
python3 pysql/main_c.py
```

## Commands

List of available commands

```
ALL COMMANDS

    select          TB_NAME, COLUMNS, ARGS      Displays selected columns of a table
    insert -s       TB_NAME, ARGS               Insert a single row in a table
           -m       TB_NAME, NUM, ARGS          Insert `NUM` rows in a table
           -f       TB_NAME, FILE_NAME          Insert values in a table from CSV file
    update          TB_NAME, COLUMNS, ARGS      Updates values of columns in a table
    delete          TB_NAME, COLUMN             Deletes values of row in a table
    showdb                                      Display all databases in MySQL server
    usedb                                       Use a database
    createdb        DB_NAME                     Create a new database
    dropdb          DB_NAME                     Delete a database
    showtb                                      Display all tables in current db
    createtb        TB_NAME, ARGS               Create a new table in current db
    droptb          TB_NAME                     Delete a table in current db
    trunctb         TB_NAME                     Truncate a table in current db
    desctb          TB_NAME                     Display structure of a table in current db
    altertb         TB_NAME, ARGS               Alter contents of table in current db
    exportdb        DB_NAME, PATH               Export db as `.sql` file to path
    exporttb  -txt  TB_NAME, PATH               Export table as `.txt` file to path
              -csv  TB_NAME, PATH               Export table as `.csv` file to path
              -sql  TB_NAME, PATH               Export table schema as `.sql` file to path
    exportall -txt  PATH                        Export all tables in db as `.txt` file to path
              -csv  PATH                        Export all tables in db as `.csv` file to path
              -sql  PATH                        Export all tables schema in db as `.sql` file to path
    importdb        DB_NAME, PATH               Import `.sql` file into input database
    importtb        DB_NAME, PATH               Import `.sql` table schema into input table
```
