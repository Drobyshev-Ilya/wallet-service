from setuptools import setup, find_packages

setup(
    name="wallet-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "asyncpg",
        "pydantic",
        "python-dotenv",
    ],
)
