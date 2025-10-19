# 🎧 Podcast Web Application

A Flask-based platform for browsing, managing, and testing podcast data.

## Overview

This project is a full-stack web application developed with Flask and Python, designed to manage podcast data, perform CRUD operations, and demonstrate clean software architecture using the Model-View-Controller (MVC) pattern.

It features a structured domain model, automated unit testing, and dynamic HTML rendering via Jinja2 templates. Originally developed as part of a university project, it has been expanded and refined to highlight practical software engineering principles.

## Features

Podcast Management — Create, read, update, and delete podcast data entries.

Domain Modeling — Structured object-oriented design representing podcasts, episodes, and creators.

Dynamic Rendering — Jinja2 templates for rendering domain objects as interactive HTML pages.

Testing Suite — Automated testing framework using pytest to ensure code reliability.

Environment Configuration — Uses .env variables for development and production separation.

## Tech Stack
- Category	Tools / Frameworks
- Backend	Python, Flask
- Templating	Jinja2
- Database	SQLite
- Testing	pytest
- Version Control	Git, GitHub

## Setup & Installation

Clone the repository:

`git clone https://github.com/yourusername/podcast-webapp.git
cd podcast-webapp`

Create a virtual environment and install dependencies:

`python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
`

Run the application:

`flask run
`

Then open your browser and visit:

`http://localhost:5000`

## Running Tests

Run the automated test suite with:

`pytest`


All tests are located in the /tests directory and validate domain logic, data access, and route handling.
