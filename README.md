# RetinAi-Backend

Backend for RetinAi Project <br>

Main Purpose: <br>
&nbsp;&nbsp;&nbsp;&nbsp;Recieve images from kiosk <br>
&nbsp;&nbsp;&nbsp;&nbsp;Pre process images if needed <br>
&nbsp;&nbsp;&nbsp;&nbsp;Make request to ML model <br>
&nbsp;&nbsp;&nbsp;&nbsp;Recieve data from ML model and return this information back <br>
&nbsp;&nbsp;&nbsp;&nbsp;Store all data and images for the session<br>

## Stack

Table: SQL <br>
Language: Python <br>
Frame Work: FastAPI <br>

## Virtual Environment

1. create a virtual environment using

- `$ python -m venv .venv`

2. Activate virtual environment "venv" using

- `$ source .venv/Scripts/activate`

3. Install all required packages using

- `$ pip install -r requirements.txt`

4. Test if in venv and all requirments are there using

- `$ pip list`

5. To close venv use

- `$ deactivate`

6. Optional If adding more packages run

- `$ pip freeze > requirements.txt`

## Development

To run development use

```
$ fastapi dev main.py
```

Development runs on: http://127.0.0.1:8000

Docs are avalible on: http://127.0.0.1:8000/docs#/
