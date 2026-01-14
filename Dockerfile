FROM python:3.12.12-slim

RUN apt-get update && \
    apt-get install -y xmlsec1 && \
    apt-get clean
# ensure we have pip 25.1+ for PEP 735 dependency groups
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/ipmanager

COPY pyproject.toml .
COPY src ./src
COPY attribute-maps ./attribute-maps

RUN pip install -e . --group prod

RUN src/manage.py collectstatic

EXPOSE 3001

# Commands to run migration and start the server
CMD ["sh", "-c", "src/manage.py migrate && ipmanager"]
