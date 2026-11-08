# Enterprise Knowledge Intelligence (EKI)

An AI-powered enterprise knowledge assistant designed
to answer questions from internal documents.

## Current Features

- FastAPI backend
- Chat API endpoint
- Pydantic request validation
- Health check endpoint
- Automated API testing using Pytest

## Tech Stack

- Python
- FastAPI
- Pydantic
- Pytest

## Project Structure

- app/api: API routes
- app/core: Configuration
- app/schemas: Request and response models
- app/services: Business logic
- tests: Automated tests
- data/documents: Input documents

## Run Locally

Install dependencies:

pip install -r requirements.txt

Start server:

py -m uvicorn app.main:app --reload

Run tests:

py -m pytest -v

## API Documentation

http://127.0.0.1:8000/docs