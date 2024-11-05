## To run our Python Flask backend locally:
- Create a python virtual environment and activate it:
For Windows:
```bash 
python -m venv venv
```
```bash
venv\Scripts\activate
```
For Mac:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
- Install all packages with:
```bash
pip install -r requirements.txt
```
- Install Redis locally (NOT IN VENV)
For windows: 
1. Install WSL if you haven't
2. In local environment, do:
```bash
pip install redis
```
3. Open command prompt, do:
```bash
wsl
```
```bash
sudo service redis-server start
```
- Start your Flask app with command:
```bash
python app.py
```

## How to run our React front-end locally:
- install node.js. https://nodejs.org/en
- after installation of node.js. run the following command to install the dependencies and neccessary files for this project.
```
npm install
```
- Now you can start your frontend locally with:
```
npm start
``` 