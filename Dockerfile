FROM python:3.8

# First, we need to install Pipenv
RUN pip install pipenv

# Then, we need to convert the Pipfile to requirements.txt
COPY Pipfile* /tmp/

RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt

# Last, we install the dependency and then we can start the Gunicorn.
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/app

WORKDIR /tmp/app

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
