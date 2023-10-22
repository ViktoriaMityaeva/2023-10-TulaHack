FROM python:3.11
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /bot

COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 755 .