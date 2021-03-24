FROM python:3.9-buster
COPY ./vough_backend/ /code
EXPOSE 8000
WORKDIR  /code
RUN pip install pipenv
RUN pipenv install --system
CMD gunicorn vough_backend.wsgi