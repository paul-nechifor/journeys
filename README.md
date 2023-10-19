# Journeys

Note: I've changed `clone` in `client-b/client-b-tkr-journey.yaml` to
`client-b-thr` instead of `client-b-tkr`. The value `client-b-tkr` meant it
would be a clone of itself so it would never show up in the tree. I've changed
it to `client-b-thr` since it's the smallest correction, but also overwrites
the `joint` value from the parent (I haven't noticed any other overwrites).

## Backend

Go to the directory:

    cd backend

Install:

    poetry install

Start the server:

    poetry run uvicorn main:app --reload

It will run on <http://localhost:8000/get-journeys>.

View the docs at [localhost:8000/docs](http://localhost:8000/docs).

Run the tests:

    poetry run pytest

## Frontend

Go to the directory:

    cd frontend

Install:

    yarn

Start the dev server:

    yarn start

It will run on [localhost:3000](http://localhost:3000/).

Run the tests:

    yarn test

### End to end tests

Go to the dir:

    cd e2e

Install:

    poetry install
    poetry run playwright install

Run the tests:

    poetry run pytest
