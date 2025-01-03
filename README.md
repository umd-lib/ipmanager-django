# ipmanager-django

Django implementation of the University of Maryland Libraries' standalone
IP Manager Service. The service provides both an Administrator UI and a REST
API interface for IP lookups.

## Development Setup

```zsh
git clone git@github.com:umd-lib/ipmanager-django.git
cd ipmanager-django
python -m venv --prompt "ipmanager-django-py$(cat .python-version)" .venv
source .venv/bin/activate
pip install -e '.[test]'
```

To run the webapp using the built-in web server:

```zsh
src/manage.py runserver
```

The application will be running at <http://localhost:8000/>

To use an alternate port, specify it after the `runserver` command:

```zsh
src/manage.py runserver 5999
```

Then the application will be running at <http://localhost:5999/>

### Tests

This project uses the [pytest] test framework, in conjunction with the
[pytest-django] plugin, for testing. Tests are located in the [tests](tests/)
directory.

To run the tests:

```zsh
pytest
```

Configuration for `pytest` is maintained in the [pyproject.toml] file.

### Code Formatting and Linting

This project uses [ruff] for code format checking and code linting.

To run the linter:

```zsh
ruff check
```

To run the formatter:

```zsh
# show what would be changed without making the changes
ruff format --diff

# automatically apply the changes
ruff format
```

Configuration for `ruff` is maintained in the [pyproject.toml] file.

## History

This project began life as a Java servlet application that was tightly
integrated with the UMD Libraries' Fedora 2 digital repository application.

In 2022, it was reimplemented as a Ruby on Rails application, and expanded
to include a more user-friendly admin UI. The API was also changed from
the XML format used by the original application to a more modern JSON
implementation.

In 2025, it is being reimplemented again, this time using Python and the
Django framework.

## License

See the [LICENSE](LICENSE) file for license rights and limitations (Apache 2.0).

[pyproject.toml]: pyproject.toml
[pytest]: https://docs.pytest.org/en/stable/
[pytest-django]: https://pytest-django.readthedocs.io/en/latest/
[ruff]: https://docs.astral.sh/ruff/
