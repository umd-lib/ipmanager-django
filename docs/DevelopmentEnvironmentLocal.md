# Development Environment - Local

## Introduction

This document provides guidance on setting up an IPManager Django development environment
on a local workstation.

## Prerequisites

* Python 3.12
* Install `libxmlsec1`. This is required for the SAML authentication using
  [djangosaml2].

  On Mac, it is available via Homebrew:

  ```zsh
  brew install xmlsec1
  ```

  On Debian or Ubuntu Linux, it is available via `apt`:

  ```zsh
  sudo apt-get install xmlsec1
  ```

* Update the `/etc/hosts` file to add:

  ```zsh
  127.0.0.1 ipmanager-local
  ```

## Application Setup

1) Clone ipmanager-django from GitHub:

    ```zsh
    git clone git@github.com:umd-lib/ipmanager-django.git
    cd ipmanager-django
    ```

2) Set up the Python virtual environment, and install the dependencies

    ```zsh
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

3) Retrieve the SAML Key and Cert information. The cert file can be accessed through
   Box. Alternatively, you can pull the key and cert from the kubernetes cluster into
   a file using the following commands:

    KEY FILE
    `kubectl -n test get secret ipmanager-common-env-secret -o jsonpath='{.data.SAML_SP_PRIVATE_KEY}' | base64 --decode > ./env/ipmanager-key.key`

    CERT FILE
    `kubectl -n test get secret ipmanager-common-env-secret -o jsonpath='{.data.SAML_SP_CERTIFICATE}' | base64 --decode > ./env/ipmanager-cert.crt`

    ℹ️ Note: These files can be placed in an directory outside the project,
    if desired - just change the location of the output file. 

4) Copy the "env_example" file to ".env":

    ```zsh
    cp env_example .env
    ```

    and update the following variables with the appropriate values:

    * SAML_KEY_FILE - relative (or absolute) file path to the
      `ipmanager-key.key` file
    * SAML_CERT_FILE - relative (or absolute) file path to the
      `ipmanager-cert.crt` file
    * SECRET_KEY - Either comment out (a random key will be automatically
      generated), or populate with anything with sufficient randomness,
      i.e. `uuidgen | shasum -a 256 | cut -c-64`
    * XMLSEC1_PATH - The full file path to the "xmlsec1" binary, (usually
      findable by running `which xmlsec1`)

5) Initialize the database:

    ```zsh
    ./src/manage.py migrate
    ```

7) Run the application. The default port is 3001; this is also the port that
   is registered with DIT to allow SAML authentication to work from local:

    ```zsh
    ./src/manage.py runserver
    ```

    The application will be running at <http://ipmanager-local:3001/>

    To change the port, provide an argument to `runserver`, e.g.:

    ```zsh
    ./src/manage.py runserver 5555
    ```

### Tests

To install test dependencies, install the `test` extra:

```zsh
pip install -e '.[test]'
```

This project uses [pytest] in conjunction with the [pytest-django] plugin
to run its tests. To run the test suite:

```zsh
pytest
```

To run with coverage information:

```zsh
pytest --cov src --cov-report term-missing
```

[djangosaml2]: https://djangosaml2.readthedocs.io/
[pytest]: https://pytest.org/
[pytest-django]: https://pytest-django.readthedocs.io/en/latest/