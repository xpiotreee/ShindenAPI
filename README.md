# Shinden API
Shinden API written in python with [fastapi](https://github.com/tiangolo/fastapi) and [lxml](https://github.com/lxml/lxml).
## Installation
```
pip install -r requirements.txt
```
## Start
Normal start
```
uvicorn main:app
```
Dev start with file updating after changes
```
uvicorn main:app --reload
```
## Docs
Enter `http://127.0.0.1:8000/docs` in browser after starting.
