# Docker-Compose local setup

This application ships with a configuration that allows you to run the application locally using Docker and Postgres. 

## Setup

1. Follow step 3 under 'Application Setup' in [DevelopmentEnvironmentLocal](./DevelopmentEnvironmentLocal.md) to get the Key and Cert file into the ./env folder of the repository root.

2. Run `docker-compose up --build` to start the application.

3. Navigate to http://ipmanager-local:3001 to access the application