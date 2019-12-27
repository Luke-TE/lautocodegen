FROM ubuntu:latest

COPY . /

RUN apt-get update -y \
&& apt-get upgrade -y \
&& apt-get install -y chromium-browser python3.6 python3-pip

RUN pip3 install pipenv
RUN pip3 install -r requirements.txt

CMD ["python3.6", "src/main.py"]