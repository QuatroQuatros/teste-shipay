FROM python:3.9

WORKDIR /var/www/html

COPY . /var/www/html

RUN pip install -r requirements.txt

EXPOSE 5000

# CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "./main:app"]



