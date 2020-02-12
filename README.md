# Automated loyalty code generator

A Python script that automates the signing and completion of online email-based loyalty schemes. 
The script automates the process of signup and verification in online loyalty forms using headless Chrome and email parsing. 
The resulting loyalty code is sent to an email of your choice. 

By providing an email account to the program, the program monitors the email inboxes and continuously
handles loyalty scheme emails. Any emails to the provided email address (with a particular secret code as the subject) will
then receive a loyalty code.

For this to function correctly, IMAP and SMTP must be enabled on the email account. 

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

#### Prerequisites

As the program makes use of Python 3.7's new `asyncio` syntax, the program will only work using
 Python versions from 3.7 only. Pip is also required to install the required dependencies.
On Ubuntu, this is:
```bash
apt install python python-pip

# With explicit versions 
apt install python3.7 python3-pip
``` 

The Chrome browser is also required for headless Chrome:
```bash
apt install chromium-browser
```  

The appropriate chromedriver must also be installed:
```bash
cd lautocodegen/resources/
wget "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip" -P lautocodegen/resources/
unzip lautocodegen/resources/chromedriver_linux64.zip -d lautocodegen/resources/
```

The virtual environment tool used in this project is Pipenv:
```bash
pip install pipenv

# With explicit versions
python3.7 -m pip install pipenv
```  
However, a requirements file is provided so that alternate virtual environment tools can be used.

#### Installing

To start the virtual environment:
```bash
pipenv shell 

# With explicit versions
python3.7 -m pipenv shell
```

To install all dependencies from the Pipfile:
```bash
pipenv install
```

The script will not run without appropriate environment variables:
```
LCG_EMAIL=... # The email to be used
LCG_PASS=... # The password for the email account
LCG_LOYALTY_URL=... # The URL of the loyalty scheme
LCG_STAMPS=... # The number of stamps to receive the loyalty code
LCG_SECRET_CODE=... # The subject of incoming emails required
LCG_SENTRY_DSN=... # The DSN for sentry monitoring (optional)
```
Set these before running the script. 
For Docker deployment, these should be placed in an `env_file`.

To run the program:
```bash
python -m lautocodegen
```
This will continue to run until it receives a KeyboardInterrupt. 
To enable verbose output, run it with the flag `--verbose`.


### Deployment

The program can be containerised using Docker with the provided Dockerfile. 
The Docker container can then be deployed to any local or cloud server.

To build the Docker image:
```bash
docker build . -t lautocodegen
```

To run the Docker container with the environment variable file:
```bash
docker run --env-file env_file lautocodegen

# Access container using a Bash shell
docker run --env-file env_file -it lautocodegen bash
```

### Built With

* [Docker](https://www.docker.com/) - Container deployment
* [Pipenv](https://github.com/pypa/pipenv) - Virtual environment tool used
* [Selenium](https://selenium.dev/) - Used in headless Chrome
 

### Authors

* **Luke Texon** - *Initial work* - [Luke-TE](https://github.com/Luke-TE)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

### Acknowledgments

* GitHub User PurpleBooth for the README template
* Jason C. Mcdonald for the [guide on project structure](https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6)
