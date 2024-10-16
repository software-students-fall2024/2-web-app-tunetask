# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

For busy individuals looking to streamline their daily routines, TuneTask is a mobile website that lets users create task-based playlists.

## User stories

1. **As a new user, I want to make an account**
   - This would allow the user to add data (new user info) to the database.

2. **As a recurring user, I want to sign in**
   - This story retrieves user data from the database to verify credentials.

3. **As a user, I want to be able to view and revisit my past TuneTasks**
   - This retrieves task data from the database.

4. **As a user, I want to be able to search for my friends’ profiles and view their TuneTasks**
   - This allows the user to search for data (friends' profiles) in the database.

5. **As a user, I want to be able to make a new TuneTask**
   - This story adds new task data to the database.

6. **As a user, I want to be able to modify my saved TuneTasks in my library**
   - This allows the user to edit data in the database.

## Steps necessary to run the software

### Step 1: Set Up Your Environment

1. **Install Python**:
   - Download and install Python.

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   
3. **Activate your Virtual Environment**:

   - windows: .\venv\Scripts\activate
   
   - macOS/Linux: source venv/bin/activate

### Step 2: Install Required Packages
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Create a .env File
   ```bash
   MONGO_URI=your_mongo_connection_string
   MONGO_DBNAME=your_database_name
   FLASK_PORT=3000  # Optional: Change the port if needed
   ```

   - Replace your_mongo_connection_string and your_database_name with your actual values.

### Step 5: Run The Application
   ```bash
   python app.py
   ```
   

## Task boards

[Sprint 1](https://github.com/orgs/software-students-fall2024/projects/32/views/1)

[Sprint 2](https://github.com/orgs/software-students-fall2024/projects/33/views/1)
