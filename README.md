# Stockd

Pantry and stock inventory system built with Django and PostgreSQL (Supabase).

## Core feature: Storage and item management
Users create storages (pantry, refrigerator, freezer, store shelf) and add items
inside them. Each item has a quantity, a unit, an optional expiry date and notes.
Storages and items can be viewed, edited and deleted. Data is saved in Supabase,
and every record is linked to the user who created it.

- Customers see and manage only their own storages and items.
- Admins see totals on their dashboard and a read-only list of all storages.
- Items expiring within 7 days or already expired are flagged.

## Standard features (Project Development 1)
Registration, login/logout, role-based dashboards (admin and customer), user profile.

## Tech stack
Django (templates), PostgreSQL on Supabase, Python <version>

## Setup
1. Clone the repository: `git clone <repo url>`
2. Create and activate a virtual environment:
   `python -m venv .venv` then `.venv\Scripts\activate`
3. Install packages: `pip install -r requirements.txt`
4. Create a `.env` file next to `manage.py`:
   DB_NAME=postgres
   DB_USER=<supabase user>
   DB_PASSWORD=<supabase password>
   DB_HOST=<supabase pooler host>
   DB_PORT=5432
5. Run migrations: `python manage.py migrate`
6. Create an admin: `python manage.py createsuperuser`, then set its role to
   admin in /django-admin/
7. Start the server: `python manage.py runserver`

## Git workflow
main (stable) <- develop (integration) <- feature/<name> branches, merged by pull request.