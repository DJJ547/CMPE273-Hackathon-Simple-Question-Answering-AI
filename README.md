## To run our Python Flask backend locally:

1. **Create a Python virtual environment and activate it:**

   - **For Windows:**
     ```bash
     python -m venv venv
     ```
     ```bash
     venv\Scripts\activate
     ```

   - **For Mac:**
     ```bash
     python3 -m venv venv
     ```
     ```bash
     source venv/bin/activate
     ```

2. **Install all packages:**

   - **For Windows:**
     ```bash
     pip install -r requirements.txt
     ```

   - **For Mac:**
     ```bash
     pip3 install -r requirements.txt
     ```

3. **Install Redis locally (NOT IN VENV) and start your Redis server:**

   - **For Windows:**
     - Install the Redis Python package in the local environment:
       ```bash
       pip install redis
       ```
     - Install WSL by running this command in PowerShell as Administrator:
       ```bash
       wsl --install
       ```
     - Open Command Prompt, and run:
       ```bash
       wsl
       ```
       ```bash
       sudo apt update
       ```
       ```bash
       sudo service redis-server start
       ```

   - **For Mac:**
     - Install Redis with Homebrew:
       ```bash
       brew install redis
       ```
     - Start the Redis server:
       ```bash
       brew services start redis
       ```

4. **Start your Flask app:**

   ```bash
   python app.py


## How to run our React front-end locally:

1. **Install Node.js**:
   - Download and install Node.js from [https://nodejs.org/en](https://nodejs.org/en).

2. **Install dependencies**:
   - After installing Node.js, navigate to your project directory and run:
     ```bash
     npm install
     ```

3. **Start the front-end**:
   - Start your React application locally with:
     ```bash
     npm start
     ```