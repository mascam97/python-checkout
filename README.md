# **P2PCheckout Python Integration Library**

[![codecov](https://codecov.io/github/andrextor/P2PCheckout/graph/badge.svg?token=XPxrdb1Q2M)](https://codecov.io/github/andrextor/P2PCheckout)

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

## **Installation**

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/andrextor/P2PCheckout.git
cd P2PCheckout

python -m venv env
source env/bin/activate # In Windows: env\Scripts\activate
pip install -e ".[dev]"  # For development
```

This will install the library in editable mode and include all development dependencies like flake8, pytest, and pytest-cov.

## ***Quick Start For Production Use **

Here’s a quick example to get you started with the library:

1.Configuration

Set up your Settings object with the necessary credentials:

```python
from entities.settings import Settings
from src.p2p_checkout import P2PCheckout

# Configuration
config = {
    "baseUrl": "https://example.placetopay.com/redirection/",
    "login": "your_login",
    "tranKey": "your_transaction_key",
    "timeout": 10,
    "verifySsl": True, # Default=True
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

Project Structure

P2PCheckout/
├── src/
│   ├── entities/      # Core models (e.g., Account, Status, Settings)
│   ├── messages/      # Handles request and response models
│   ├── exceptions/    # Custom exceptions
│   ├── client/        # HTTP client logic (e.g., RestCarrier)
│   ├── contracts/     # Interfaces for reusable components
├── tests/             # Unit tests and integration tests
│   ├── unit/
│   ├── features/
├── .coveragerc        # Coverage configuration
├── pytest.ini         # Pytest configuration
├── README.md          # Project documentation
├── setup.py           # Installation script

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
