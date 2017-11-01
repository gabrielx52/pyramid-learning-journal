# Pyramid Learning Journal

A simple Pyramid daily learning journal app.

**Authors**:

- Gabriel Meringolo (gabriel.meringolo@gmail.com)


## Routes:

- `/` - the home page and a listing of all posts
- `/journal/new-entry` - to create a new journal entry
- `/journal/{id:\d+}` - the page for an individual entry
- `/expense/{id:\d+}/edit-entry` - for editing existing entries 

## Set Up and Installation:

- Clone this repository to your local machine.

- Once downloaded, `cd` into the `pyramid-learning-journal` directory.

- Begin a new virtual environment with Python 3 and activate it.

- `cd` into the next `learning_journal` directory. It should be at the same level of `setup.py`

- `pip install` this package as well as the `testing` set of extras into your virtual environment.

- `$ pserve development.ini --reload` to serve the application on `http://localhost:6543`

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following:

```
$ py.test learning_journal
```
