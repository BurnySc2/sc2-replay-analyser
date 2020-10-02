[![Actions Status](https://github.com/BurnySc2/python-template/workflows/RunTests/badge.svg)](https://github.com/BurnySc2/python-template/actions)

# python-template
Template for any of my upcoming Python projects


# Useful Poetry commands
https://python-poetry.org/docs/cli/
### Create new project
`poetry init`

or

`poetry new <project-name>`
### Install dependencies
`poetry install`

`poetry install --no-dev`
### Add dependencies
`poetry add <package-name>`

Add dev dependency:

`poetry add <package-name> --dev`
### Remove dependencies
`poetry remove <package-name>`
### Update dependencies
`poetry update`
### List of packages
`poetry show`
### Validate pyproject.toml
`poetry check`
### Build
`poetry build`
### Publish
`poetry publish`
### Run a file
`poetry run pytest`

`poetry run main.py`
### Write requirements.txt from Poetry lock file
`poetry export -f requirements.txt > requirements.txt`


# Run python files
- install `poetry` using command `pip install poetry`
- run the python file `main.py` using `poetry run main.py`
- or `poetry shell` and then run `main.py`


# Run Tests
Single file:
`poetry run pytest test/test_functions.py`

Test all files in folder:
`poetry run pytest test/`




