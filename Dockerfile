FROM ubuntu:latest

COPY . /

RUN apt-get update -y \
&& apt-get install -y chromium-browser python3.7 python3-pip

RUN python3.7 -m pip install -r requirements.txt

CMD ["python3.7", "-m", "lautocodegen"]