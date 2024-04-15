# Tasker

Rest API for Tasker Webapp

## Running Locally

To run this application locally, follow these steps:

#### Prerequisites

- Python 3.x installed on your machine
- Pip package manager installed
- Virtualenv installed

#### Setting up Virtual Environment

1. Clone this repository to your local machine:

   ```bash
   git clone -b branch_name <repository address>
   ```

2. Navigate to the project directory:

   ```bash
   cd tasker/server
   ```

3. Create a virtual environment:

   ```bash
   python -m venv env
   ```

4. Activate the virtual environment (on Windows):

   ```bash
   env\Scripts\activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### Running the Application

1. Make migrations:

   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations:

   ```bash
   python manage.py migrate
   ```

3. Run the server:

   ```bash
   python manage.py runserver
   ```

4. Access the application in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)