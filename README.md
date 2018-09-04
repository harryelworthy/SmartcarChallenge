# Smartcar Coding Challenge
### Created by Harry Elworthy

This is a flask web app designed to fulfill the API requirements set out in a 3 day coding challenge for Smartcar. Following PEP8.

## Quickstart Instructions

Python3 required. 

### Install server and requirements
Download, navigate to the directory and run:
``` bash
mkdir venv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Run server
``` bash
python server.py
```
The API server should be live on localhost.


Note! Pip is broken on most recent MacOS releases (?) and I had to run the following to get it working: 
```bash
curl https://bootstrap.pypa.io/get-pip.py | python
```

For testing run in base folder:
```bash
py.test
```

Important code files are server.py and /tests/test_sc.py. Test JSON files are stored in /tests.

## TODOs
* Clean up
** Check requirements and trim down
* Go through errors
** Make sure all possible errors are handled
** Evaluate whether I'm handling correctly
** Add tests for errors