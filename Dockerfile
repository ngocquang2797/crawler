FROM python:3.8-slim-buster
#FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # install tor
  && apt install -y tor \
  # translations dependencies
  && apt-get install -y gettext \
  # Google Chrome installation dependencies
  && apt-get install -y wget gnupg curl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

#RUN service tor start
#
#RUN sh -c 'echo "ControlPort 9051" >> /etc/tor/torrc' \
# && sh -c 'echo "CookieAuthentication 1" >> /etc/tor/torrc' \
# && service tor restart

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN pip install requests
RUN pip install requests[socks]
RUN pip install requests[security]

# install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install ChromeDriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

RUN chmod 777 /usr/local/bin/chromedriver

# expose display to X11
ENV DISPLAY=:99

WORKDIR /app