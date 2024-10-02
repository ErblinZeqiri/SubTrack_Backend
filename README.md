# Subtrack Backend

This repository contains the backend code for the **Subtrack** application, a subscription management platform. The backend is built using **Python** and the **Flask** framework, providing a RESTful API for managing users, subscriptions, and authentication.

## Features

- **User Management**: Register, login, and secure user data with password hashing and JWT-based authentication.
- **Subscription Management**: Add, list, and manage subscriptions for authenticated users.
- **Data Validation**: Ensure data integrity with model validation for all user and subscription data.
- **Security**: Implement JWT tokens for secure authentication and role-based access control.

## Technologies

- **Python**: Core programming language.
- **Flask**: Web framework for creating RESTful APIs.
- **JWT**: Used for user authentication and session management.
- **SQLAlchemy**: ORM for database interaction (optional, replace with your database layer).
- **SQLite/PostgreSQL/MySQL**: Example databases for local or production use.

## Project Structure

```bash
backend/
│
├── config/          # Configuration files for the application
├── controllers/     # API route controllers for users and subscriptions
├── models/          # Database models and schemas for users and subscriptions
├── services/        # Business logic and data manipulation
├── utils/           # Utility functions (e.g., token generation, password hashing)
├── app.py           # Main entry point for the Flask application
└── requirements.txt # Dependencies for the project
```

### Setup

##### 1. Clone the repository:
    git clone https://github.com/ErblinZeqiri/subtrack-backend.git

##### 2. Install dependencies:

    conda env create -f environment.yml

#### 3. Configure environment variables (e.g., database URL, secret keys).

#### 5. Run the application:

    python app.py

API Endpoints

    /auth/register - Register a new user
    /auth/login - Log in an existing user
    /subscriptions - Manage subscriptions for authenticated users
