# Door_Unlock_Web_GUI
Web application to manage Pitt RAS Door Unlocker

Powered by VueJS, Flask and SQLite

## Setup

To contribute to the project, you should have the following installed:

- NodeJS (Frontend)
- Python (Backend)
    * `pipenv` is also needed
- SQLite (min. version 3.10 and above)

### Backend
Backend setup is straightforward, simply navigate to `src/backend` and run
`pipenv install` and then `pipenv shell` to install the python dependencies
and initialize the virtual environment

## Frontend
Frontend is a little more involved, as the Vue-CLI must be installed first. Run `npm install -g @vue/cli` to install the necessary tooling. From there, navigate to `src/frontend` and run `npm install` to install all related dependencies. For more info about working VueJS and the Vue-CLI, please consult
the appropriate documentation.

## General Info and Design Notes

The Web GUI is the primary means of managing users for the Door Unlocker system.
The GUI is a Vue.JS SPA backed by a REST API powered by Python/Flask and uses
SQLite as its presistence layer. For those familiar with SQLite and its quirks,
note that the intention is to have foreign keys enforced and thus all
transactions must be preceded with `PRAGMA foreign_keys = ON`
