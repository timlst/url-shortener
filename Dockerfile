FROM python:3.8-alpine

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

COPY shortist/ .

CMD ["flask", "init-db"]
CMD ["flask", "register-user", "username", "password"]
CMD ["waitress-serve", "--call", "shortist:create_app"]