# Inquest-auth

**Inquest-auth** is a microservice for handling user authentication, authorization, and user management in the Inquest survey management system. It provides the necessary endpoints and logic for managing user accounts and securing access to other microservices.

## Features

- **User Registration**: Allows new users to create accounts.
- **User Login**: Authenticates users and provides JWT tokens for secure access.
- **Token Validation**: Validates JWT tokens to ensure secure access to protected resources.
- **User Management**: Provides endpoints for managing user information.

## Project Structure

- **`src/`**: Contains the source code for the microservice.
  - **`controllers/`**: Contains the route handlers and controllers.
  - **`schemas/`**: Defines Pydantic models for request and response validation.
  - **`utils/`**: Contains utility functions and classes, including JWT utilities.
  - **`env/`**: Configuration files and environment settings.

## Setup Instructions

### Prerequisites

- Ensure you have [Git](https://git-scm.com/) installed on your machine.
- Install [Python](https://www.python.org/) (version 3.8 or higher) and [pip](https://pip.pypa.io/en/stable/).

### Cloning the Repository

Clone the `Inquest-auth` repository:

```bash
git clone https://github.com/Dun-Njuguna/inquest-auth.git
cd inquest-auth
```

### Installing Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the root directory and add the necessary environment variables. Example:

```env
# Common settings
APP_NAME=inquest-auth
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=

# Database configurations
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

### Running the Microservice

Start the FastAPI application using Uvicorn:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Login a user and get a JWT token.
- **GET /auth/me**: Get the current user’s information (requires authentication).

### Contributing

If you want to contribute to the `Inquest-auth` microservice, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a clear message.
4. Push your changes and create a pull request.

### License

This project is licensed under the [MIT License](LICENSE).