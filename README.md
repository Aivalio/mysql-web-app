<div align="center">

# ✈️ Flight Search App

**A Flask web application for querying an airline database — multi-table SQL joins, admin panel, and deployed live.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![pytest](https://img.shields.io/badge/tests-14%20passed-brightgreen?logo=pytest&logoColor=white)](#-testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📖 About

A web app that exposes **5 analytical queries** over a pre-existing airline database (8 tables, 3NF).

Built as a portfolio project to practice **Flask blueprints**, **SQLAlchemy ORM** with complex JOINs, **role-based access**, and **production-style config**.

**The database is pre-existing.** The value of this project is the application layer: clean architecture, testability, and safe handling of multi-table queries.

---

## ✨ Features

| Query | Description |
|---|---|
| 👥 **Airline by Age** | Airline with the most passengers in a given age range |
| 🛬 **Airport Visitors** | Distinct passenger count per airport, for an airline + date range |
| 🔀 **Alternative Flights** | Flights between two cities on a specific date (active airlines only) |
| 🏆 **Largest Airlines** | All airlines ranked by fleet size and flight count |
| ⭐ **Update Passenger Tiers** | Admin-only: recalculate loyalty tiers (Basic/Silver/Gold/Platinum) |

**Plus:**
- 🔐 Admin authentication (bcrypt-hashed credentials via env vars)
- 📱 Responsive layout with a shared base template
- ⚠️ Flash messages for errors and empty results
- ✅ Form validation (ranges, date ordering, required fields)

---

## 🏗️ Architecture

Clean 3-layer architecture following the **Single Responsibility Principle**:



**Design principles:**
- **Routes know nothing about SQL.** They call services.
- **Services know nothing about Flask.** They call models.
- **Models know nothing about business rules.** They define structure only.
- **Everything is testable** with an in-memory SQLite DB.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Web** | Flask 3.0 | Blueprints, sessions, forms |
| **ORM** | Flask-SQLAlchemy 3.1 | Typed models, complex JOINs |
| **DB** | MySQL 8 + PyMySQL | Existing relational schema |
| **Auth** | Flask-Login + Werkzeug | Session-based admin login |
| **Config** | python-dotenv | Env vars for secrets |
| **Templates** | Jinja2 | Base + page inheritance |
| **Tests** | pytest + SQLite in-memory | 14 unit tests |

---

## 🚀 Live Demo

👉 **[mysql-web-app.onrender.com](https://mysql-web-app.onrender.com/)**
---

## 📦 Installation

### Prerequisites

- Python 3.11+
- **MySQL 8** running locally (XAMPP, MySQL Installer, or Docker)
- The `flights` database already imported

### 1. Clone

```bash
git clone https://github.com/Aivalio/mysql-web-app.git
cd mysql-web-app
```



**Design principles:**
- **Routes know nothing about SQL.** They call services.
- **Services know nothing about Flask.** They call models.
- **Models know nothing about business rules.** They define structure only.
- **Everything is testable** with an in-memory SQLite DB.

---


### 2. Virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure secrets

```bash
# Windows
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env` and set your MySQL credentials:

```
SECRET_KEY=<random 64-char hex>
FLASK_DEBUG=True
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=flights
DATABASE_URL=mysql+pymysql://root:your_password_here@localhost:3307/flights
```

Generate a `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Generate an admin password hash:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your_admin_password'))"
```

Paste the result into `ADMIN_PASSWORD_HASH` in `.env`.

> ⚠️ **Never commit `.env`.** It is ignored by Git.

### 5. Run the app

```bash
python run.py
```

Open http://127.0.0.1:5000

---

## 🧪 Testing

```bash
pytest tests/ -v
```

**Coverage:** 14 tests, using an in-memory SQLite DB with deterministic fixtures.

| File | What's tested |
|---|---|
| `test_airline_service.py` | Age-range query, no results, airline ranking |
| `test_flight_service.py` | Active-airline filter, unknown city, distinct passenger count |
| `test_passenger_service.py` | Tier boundaries, update flow, unknown airline, get-by-tier |
| `test_auth_service.py` | Wrong user, wrong password, success, unconfigured hash |

**Test design:**

- **In-memory SQLite** → instant, isolated per test
- **Fixtures in `conftest.py`** → shared setup, deterministic data
- **Business rules** tested explicitly (`active='Y'`, tier boundaries)

---

## 📁 Project Structure

```
mysql-web-app/
├── src/
│   ├── __init__.py                  # Flask app factory
│   ├── config.py                    # Config + TestConfig
│   ├── extensions.py                # db, login_manager
│   ├── models/
│   │   ├── __init__.py
│   │   ├── associations.py          # airlines_has_airplanes, flights_has_passengers
│   │   ├── airline.py
│   │   ├── airplane.py
│   │   ├── airport.py
│   │   ├── route.py
│   │   ├── flight.py
│   │   └── passenger.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── airline_service.py
│   │   ├── flight_service.py
│   │   ├── passenger_service.py
│   │   └── auth_service.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py                  # Home + 4 queries
│   │   ├── auth.py                  # Login / logout
│   │   └── admin.py                 # Tier update (auth-protected)
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── airline_by_age.html
│   │   ├── airport_visitors.html
│   │   ├── alternative_flights.html
│   │   ├── largest_airlines.html
│   │   ├── auth/
│   │   │   └── login.html
│   │   └── admin/
│   │       └── update_tiers.html
│   └── static/
│       └── style.css
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_airline_service.py
│   ├── test_flight_service.py
│   ├── test_passenger_service.py
│   └── test_auth_service.py
├── run.py                           # Dev server entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Security Notes

- **Credentials** are loaded from `.env` — never hardcoded.
- **Admin password** is stored as a Werkzeug hash (scrypt by default).
- **SQL injection** is impossible: all queries use SQLAlchemy ORM with bound parameters.
- **Admin routes** are protected with `@login_required`.
- **Cross-table queries** are isolated per-request via the Flask app context.

---

## 🗺️ Roadmap

- [ ] Add caching for the "Largest Airlines" query
- [ ] Expose the same data as a REST API (Flask-RESTful)
- [ ] Alembic migrations for schema evolution
- [ ] Dockerfile + docker-compose for one-command setup
- [ ] Pagination for large result sets
- [ ] Export results as CSV

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">

**Built with ☕ and curiosity by [Aivalio](https://github.com/Aivalio)**

⭐ If you found this useful, consider giving it a star!

</div>