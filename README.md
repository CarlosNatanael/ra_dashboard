# RA Dashboard (RetroAchievements Review Queue)

`ra_dashboard` is a prototype web application built in Python/Flask to provide a centralized and public-facing dashboard for the RetroAchievements Jr. Developer review queue.

This tool was created to solve the visibility problem for both Jr. Developers (who want to know the status of their submissions) and Code Reviewers (who need a simple tool to manage the queue).

## Features

### 1. Public View (Jr. Dev View)
* **Global Queue:** A public, read-only view showing all sets currently in the review process (i.e., not yet "Approved").
* **Search/Filter:** Users can search the queue by Game Name or Developer.
* **History Page:** A separate page showing a log of all sets that have been "Approved".
* **Status Meaning:** A static page explaining what each review status (e.g., "Pending", "In_Discussion") means.

### 2. Admin View (Code Reviewer View)
* **Secure API Login:** Admins (Code Reviewers) log in using their official RetroAchievements Username and Web API Key.
* **Role-Based Access:** The backend validates the credentials against the RA API (`API_GetUserSummary.php`) and grants access only to users with a Role ID of 5 (Reviewer) or higher.
* **Full Queue Management:** Once logged in, admins can:
    * Add new games to the review queue.
    * Update the status of any set (e.g., to "In_Review", "Approved").
    * "Claim" a set, assigning their username as the reviewer.
    * Delete entries from the queue.
* **RA API Integration:** When adding a new set, the admin only needs the Game ID. The app automatically calls the RA API (`API_GetGame.php`) to fetch the correct Game Title.

## Technology Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, (vanilla) JavaScript
* **Key Libraries:** `requests` (for API calls), `Flask-Babel` (for i18n support).

## Local Setup & Installation

To run this project on your local machine:

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/CarlosNatanael/ra_dashboard.git](https://github.com/CarlosNatanael/ra_dashboard.git)
    cd ra_dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # On Windows
    py -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt 
    ```
   

4.  **Initialize the database:**
    This app includes a CLI command to set up the `database.db` file from the schema.
    ```sh
    # On macOS/Linux
    export FLASK_APP=app.py
    flask init-db
    
    # On Windows
    set FLASK_APP=app.py
    flask init-db
    ```
    You should see a message: "Banco de dados inicializado."

5.  **Run the application:**
    ```sh
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for full details.
