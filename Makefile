PY = venv/Scripts/python

run:
    $(PY) -m pysql.main

run_c:
    $(PY) -m pysql.main_c

clean:
    $(PY) -m pyclean .
