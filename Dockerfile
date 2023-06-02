FROM node:18 AS build-stage

WORKDIR /react-app
COPY react-app/. .

# You have to set this because it should be set during build time.
ENV REACT_APP_BASE_URL=https://plz-hire-me.herokuapp.com/

# Build our React App
RUN npm install
RUN npm run build

FROM python:3.9

# Install NLTK and download data
RUN pip install nltk
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger

# Setup Flask environment
ENV FLASK_APP=app
ENV FLASK_ENV=production

EXPOSE ${PORT:-5003}

WORKDIR /var/www
COPY . .
COPY --from=build-stage /react-app/build/* app/static/

# Install Python Dependencies
WORKDIR /var/www/app

RUN pip install -r requirements.txt

# Run flask environment
ENV WORKERS=3
CMD gunicorn -b 0.0.0.0:${PORT:-5003} -t 1800 -w $WORKERS app:app
