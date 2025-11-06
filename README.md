# FastAPI Address Book — Complete Project

This repository contains a complete, production-minded FastAPI project implementing the Eastvantage assignment: an address book with CRUD operations, SQLite persistence, validation, and a nearby-addresses query by distance.

---

## File index (contents included below)

* `README.md`
* `requirements.txt`
* `docker-compose.yml`
* `database.py`
* `models.py`
* `schemas.py`
* `crud.py`
* `utils.py`
* `main.py`

---

---

# README.md

````markdown
# FastAPI Address Book

## Overview
A FastAPI application that stores addresses (with latitude/longitude) in SQLite, supports create/read/update/delete, and returns addresses within a radius from given coordinates.

## Quickstart

1. Create and activate virtualenv:

```bash
python -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn main:app --reload
```

Open docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



## API Endpoints (short)

* `POST /addresses/` create
* `GET /addresses/` list (supports `limit` & `offset`)
* `GET /addresses/{id}` retrieve
* `PUT /addresses/{id}` update
* `DELETE /addresses/{id}` delete
* `GET /addresses/nearby/?lat=...&lon=...&radius_km=...` find nearby

## Notes

* Uses SQLAlchemy ORM with SQLite.
* Pydantic validation on inputs (latitude/longitude bounds).
* Uses `geopy` for geodesic distance.
* Basic logging present.
