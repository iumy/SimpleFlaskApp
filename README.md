# **SimpleFlaskApp**
Repository for DevOps Software Engineering Assignment

## Introduction and jobs
This repository contains the source code for a Flask To Do Application developed in Python.
A GitHub Actions pipeline has been created to manage the entire workflow.
The following Jobs have been added to the Pipeline:
- Lint: this job runs Black, Flake8 and Pylint to check for correct formatting and code quality
- Unit Tests: this job runs unit tests and code coverage using pytest
- SonarQube Code Analysis: this job runs SonarQube scan to check for code quality (Gate check is only executed on main branch due to limitation of free account)
- Build Docker Image: this job builds a Docker image for the application and pushed it to GitHub Docker Registry
- Deploy to Staging: this job runs on a self hosted runner, pull the image and create/run a container to test the app. A health check is executed to confirm the app is running in the container 
- Build App: this jobs builds the python application (even though it would not be stricly required) and save the package in artifacts. This runs only on main
- Deploy to Production: this job deploys the application to an EC2 instance and check that is responding to requests.

## Monitoring
Monitoring has been implemented using Prometheus and Grafana
Blackbox and Json Exporters have been used to scrape the App root and health routes.
