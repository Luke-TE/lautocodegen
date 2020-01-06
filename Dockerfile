FROM ubuntu:latest

COPY . /

RUN apt-get update -y \
&& apt-get install -y chromium-browser python3.7 python3-pip unzip

RUN python3.7 -m pip install -r requirements.txt

ADD https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip lautocodegen/resources/chromedriver_linux64.zip
RUN unzip lautocodegen/resources/chromedriver_linux64.zip -d lautocodegen/resources/

CMD ["python3.7", "-m", "lautocodegen"]