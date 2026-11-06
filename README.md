
# PhishGuard AI - AI-Powered Phishing URL Detection System

## 1. About the Project

PhishGuard AI is an AI-powered phishing URL detection system that identifies whether a given website URL is legitimate or potentially phishing.

Phishing websites are created by attackers to steal sensitive information such as passwords, banking details, and personal data.

This project uses Machine Learning to analyze URL patterns and predict whether a URL is safe or suspicious.

The system provides a simple web dashboard where users can enter a URL and get the prediction result.

## 2. Key Features

- AI-based phishing URL detection.
- Machine Learning model using TF-IDF and Logistic Regression.
- Real-time URL scanning through a web interface.
- FastAPI backend for handling predictions.
- PostgreSQL database for storing scan history.
- Dashboard showing scan statistics.
- Search and filter options for previous scans.
- REST API with Swagger documentation.
- Automated API testing using Pytest.
- Docker support for running the complete application.

## 3. Technologies Used

Frontend:
- React.js
- Vite
- CSS
- Recharts

Backend:
- Python
- FastAPI
- Pydantic

Machine Learning:
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- Joblib

Database:
- PostgreSQL
- SQLAlchemy

Testing:
- Pytest

DevOps and Deployment:
- Docker
- Docker Compose
- Git
- GitHub

## 4. Machine Learning Model

PhishGuard AI uses a character-level TF-IDF vectorizer combined with a Logistic Regression classifier.

The model learns patterns from website URLs and uses those patterns to classify URLs into two categories:

- Legitimate: The URL is predicted to be legitimate.
- Phishing: The URL is predicted to be potentially dangerous.

Dataset used:
PhiUSIIL Phishing URL Dataset from the UCI Machine Learning Repository.

Dataset information:
- Total records: 235,795
- Legitimate URLs: 134,850
- Phishing URLs: 100,945

The model achieved approximately 99.66% accuracy on the held-out test split used during evaluation.

Note: This accuracy is based on the dataset split and does not guarantee the same performance on real-world URLs.

Dataset source:
https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset

## 5. How the Project Works

1. The user enters a website URL in the frontend.
2. React sends the URL to the FastAPI backend.
3. The backend passes the URL to the trained Machine Learning model.
4. The model analyzes the URL and predicts whether it is phishing or legitimate.
5. The prediction result is displayed on the dashboard.
6. The scan details are stored in the PostgreSQL database.
7. Users can view previous scans and dashboard statistics.

Important: The system analyzes the URL text. It does not open or visit the submitted website.

## 6. Project Structure

PhishGuard-AI/

- backend/
  - main.py
  - database.py
  - models.py
  - Dockerfile

- frontend/
  - src/
  - public/
  - Dockerfile

- ml/
  - train_url_model.py
  - phishguard_url_model.pkl

- dataset/
  - download_dataset.py
  - selected_features.csv

- tests/
  - test_api.py

- deployment/

- docker-compose.yml
- requirements.txt
- .env.example
- .gitignore
- README.md

## 7. How to Run the Project Locally

Prerequisites:

- Python installed
- Node.js and npm installed
- PostgreSQL installed
- Git installed

Step 1: Clone the repository

git clone https://github.com/Lavanyakapoor12/PhishGuard-AI.git

Step 2: Open the project folder

cd PhishGuard-AI

Step 3: Create a Python virtual environment

python -m venv venv

Step 4: Activate the environment

Windows:

venv\Scripts\activate

Step 5: Install Python dependencies

pip install -r requirements.txt

Step 6: Configure environment variables

Create a .env file in the root folder.

Add your own PostgreSQL database details:

DB_USER=your_database_username
DB_PASSWORD=your_private_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=phishguard_db

Step 7: Start the backend

uvicorn backend.main:app --reload

Backend URL:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

Step 8: Start the frontend

Open another terminal.

cd frontend

Install frontend dependencies:

npm install

Start the frontend:

npm run dev

Frontend URL:
http://localhost:5173

## 8. Run Using Docker

Docker makes it possible to run the frontend, backend, and database together.

Make sure Docker Desktop is installed and running.

From the project root folder, execute:

docker compose up -d --build

To check running containers:

docker compose ps

To view backend logs:

docker compose logs backend --tail 40

Open the application:

Frontend:
http://localhost:5173

Backend:
http://localhost:8000

API documentation:
http://localhost:8000/docs

To stop the containers:

docker compose down

## 9. Testing

The project includes automated API tests using Pytest.

The tests cover:

- Home endpoint.
- Valid URL prediction.
- Invalid URL handling.
- Scan history.
- Dashboard statistics.
- Empty URL validation.
- Missing URL validation.
- JavaScript URL validation.
- File URL validation.
- Maximum URL length validation.

Run the tests using:

python -m pytest tests/test_api.py -v

Current test result: 10 tests passed.

## 10. Security Considerations

- The system analyzes URL text without visiting the submitted website.
- URL input is validated before prediction.
- Maximum URL length is restricted to 2048 characters.
- Database credentials are stored in environment variables.
- The .env file should never be uploaded to GitHub.
- Machine Learning predictions are not a guarantee that a website is safe.

## 11. Future Improvements

- Deploy the application on a cloud platform.
- Improve model performance on previously unseen domains.
- Add more advanced phishing detection techniques.
- Implement user authentication.
- Add detailed security reports.
- Set up CI/CD using GitHub Actions.
- Add application monitoring and logging.

## 12. Author

Lavanya Kapoor

B.Tech Student - Computer Science

GitHub:
https://github.com/Lavanyakapoor12

Project:
PhishGuard AI - AI-Powered Phishing URL Detection System
