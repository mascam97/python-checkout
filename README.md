# **P2PCheckout Python Integration Library**

[![codecov](https://codecov.io/github/andrextor/P2PCheckout/graph/badge.svg?token=XPxrdb1Q2M)](https://codecov.io/github/andrextor/P2PCheckout)
[![Build Status](https://github.com/andrextor/P2PCheckout/actions/workflows/python-app.yml/badge.svg)](https://github.com/andrextor/P2PCheckout/actions)

This project is a Python library inspired by the [PlaceToPay PHP Redirection Library](https://github.com/dnetix/redirection). It aims to provide a robust and easy-to-use solution for integrating with PlaceToPay's payment gateway using Python. The library incorporates some enhancements to better fit Python's ecosystem and leverages modern Python tools like Pydantic and Requests for validation and HTTP handling.

---

## **Features**

- 🛠 **Inspired by Dnetix PHP Library**: A Python adaptation of the official PHP library, keeping the core concepts and enhancing usability.
- 🔑 **Authentication Management**: Easily handle login and transaction keys with dynamic nonce and seed generation.
- 📡 **Request Handling**: Create, query, collect, and reverse payment requests with ease.
- ✅ **Validation with Pydantic**: Ensures data integrity and validation throughout the library.
- 🌐 **HTTP Client Integration**: Built on top of the `requests` library for simplicity and flexibility.
- 🔍 **Logging**: Built-in logging to trace requests and responses.

---

## **Technologies Used**

- **Python 3.13+**
- **Pydantic**: For model validation and serialization.
- **Requests**: For HTTP client requests.
- **Logging**: To log and debug processes.
- **Typing**: To ensure type safety and better developer experience.

---

## ***Quick Start For Production Use***

Here’s a quick example to get you started with the library:

1.Configuration

Set up your Settings object with the necessary credentials:

```python
from src.p2p_checkout import P2PCheckout

# Configuration
config = {
    "base_url": "https://example.placetopay.com/redirection/",
    "login": "your_login",
    "tranKey": "your_transaction_key",
    "timeout": 10,
    "headers": {"Accept": "application/json", 'Content-Type': 'application/json'},
}

p2p_checkout = P2PCheckout(**config)
```

2.Create a Payment Request

```python
from messages.requests.redirect import RedirectRequest
from messages.responses.redirect import RedirectResponse

redirect_request = RedirectRequest(
    amount={"currency": "COP", "total": 10000},
    payment={"reference": "TEST123", "description": "Test Payment"}
)

# This request returns a `RedirectResponse` object containing the process URL.
response: RedirectResponse = placeto_pay.request(redirect_request)

print("Redirect to:", response.process_url)
```

3.Query a Payment Request

```python
from messages.responses.information import RedirectInformation

# Query a session by request ID. Returns a `RedirectInformation` object.
query_response: RedirectInformation = placeto_pay.query(123456)  # Replace with your request ID

print("Request Status:", query_response.status)
```

4.Reverse a Payment

```python
from messages.responses.reverse import ReverseResponse

# Reverse a transaction. Returns a `ReverseResponse` object.
reverse_response: ReverseResponse = placeto_pay.reverse("internal_reference")

print("Reverse Status:", reverse_response.status)
```

## **Installation**

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/andrextor/P2PCheckout.git
cd P2PCheckout
```

Install Poetry (if not already installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install dependencies

```bash
poetry install
```

To activate the development environment

- Centralized Virtual Environments: By default, Poetry places the virtual environments in a central location for all Poetry-managed projects:
~/.cache/pypoetry/virtualenvs/
- Project-Specific Virtual Environments: If you prefer the virtual environment to be created within your project directory (e.g., ./.venv), you can configure Poetry to do so:

```bash
poetry config virtualenvs.in-project true
```

```bash
poetry shell
```

Running Tests

```bash
poetry run pytest --cov=src
```

Use the following commands for code formatting and linting:

```bash
poetry run black .
poetry run flake8
poetry run isort .
```

Run type checks using mypy:

```bash
poetry run mypy src
```

Adding Dependencies

```bash
# To add a runtime dependency
poetry add <package_name> 

# To add a development dependency
poetry add --group dev <package_name>
```

Project Structure

- entities: Contains core models like Settings, Authentication, and payment-related entities (Amount, Transaction, etc.).
- messages: Handles request and response objects for PlaceToPay interactions.
- exceptions: Custom exception handling for the library.
- client: Handles HTTP client interactions, including RestCarrier.
- contracts: Defines interfaces for reusable components.
- tests: Contains unit tests to ensure the library’s functionality.

Contributing

We welcome contributions! If you’d like to contribute, please fork the repository, make your changes, and submit a pull request.

Steps to Contribute:

- Fork the repository.

```bash
git fork https://github.com/andrextor/P2PCheckout.git
``````

- Create a feature branch: git checkout -b feature/new-feature.
- Commit your changes: git commit -m "Add new feature".
- Push to the branch: git push origin feature/new-feature.
- Open a pull request on GitHub.

License

This project is licensed under the MIT License. See the LICENSE file for detail
