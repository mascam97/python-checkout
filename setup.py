from setuptools import setup, find_packages

setup(
    name="p2p_checkout",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "annotated-types==0.7.0",
        "certifi==2024.8.30",
        "charset-normalizer==3.4.0",
        "idna==3.10",
        "iniconfig==2.0.0",
        "packaging==24.2",
        "pluggy==1.5.0",
        "pydantic==2.10.0",
        "pydantic_core==2.27.0",
        "pytest==8.3.3",
        "python-dotenv==1.0.1",
        "requests==2.32.3",
        "setuptools==75.6.0",
        "typing_extensions==4.12.2",
        "urllib3==2.2.3",
    ],
    extras_require={
        "dev": [
            "flake8",
            "pytest",
            "pytest-cov",
        ],
    },
    description="Python library for PlaceToPay integration.",
    long_description=open("README.md", encoding="utf-8").read(),  # Asegúrate de usar UTF-8
    long_description_content_type="text/markdown",
    author="Iván Andrés López Gómez",
    author_email="ialopez11012@gmail.com",
    url="https://github.com/andrextor/P2PCheckout",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)