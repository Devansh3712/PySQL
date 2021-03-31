<center>
<img src = "https://user-images.githubusercontent.com/58616444/113156144-57560f80-9257-11eb-85a1-1b834c072454.png">
</center>

<h1 align = "center"> PySQL </h1>
<p align = "center"> GUI & Python wrapper for making MySQL queries easier </p>

<p align = "center">
  <a href = "www.python.org"><img src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href = "https://www.mysql.com/"><img src="https://camo.githubusercontent.com/4524c09f8c821218b3c602e3e5a222ce00c290c2f87e264b40f398a6b486bd91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6d7973716c2d2532333030303030662e7376673f267374796c653d666f722d7468652d6261646765266c6f676f3d6d7973716c266c6f676f436f6c6f723d7768697465"/></a>
  <a href = "./LICENSE"><img src = "https://img.shields.io/github/license/Devansh3712/PySQL?style=for-the-badge"></a>
</p>

---

```
PySQL
  └── pysql
      ├── __init__.py
      ├── data
      │   ├── __init__.py
      │   ├── export.py
      │   ├── imports.py
      │   ├── info.py
      │   └── logs.py
      ├── main.py
      ├── main_c.py
      └── packages
          ├── __init__.py
          ├── auth.py
          ├── ddl_commands.py
          └── dml_commands.py
```

## Installation

- Clone the repository to your local machine

```console
$ git clone https://github.com/Devansh3712/PySQL.git
```

- Automatic Setup

Open the ``PySQL`` directory, and run the setup file & activate the ``virtual environment``

> Windows

```console
> setup.cmd
> venv\Scripts\activate.bat
```

> Linux / MacOS

```console
$ chmod +x ./setup.sh
$ . setup.sh
$ source venv/bin/activate
```

- Manual Setup

Install using the dependency files

> using requirements.txt

```console
$ pip install -r requirements.txt
```

> using poetry

```console
$ poetry install
```

## Usage

- For using the Python command-line wrapper
  - ``main.py``: Basic PySQL CLI
  - ``main_c.py``: Colored PySQL CLI

> Windows

```console
> python pysql/main.py
> python pysql/main_c.py
```

> Linux

```console
$ python3 pysql/main.py
$ python3 pysql/main_c.py
```
