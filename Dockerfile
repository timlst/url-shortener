FROM python:3.8-alpine

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

COPY shortist/ .

CMD ["waitress-serve", "--call", "shortist:create_app"]