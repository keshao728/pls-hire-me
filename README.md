# Market Scope

Market Scope is a comprehensive AI-Powered Market Detective tool designed to provide insights into your competition. By leveraging modern technologies like Flask, React, OpenAI, and Google APIs, it uncovers valuable information about your competitors such as their main products or services, business strategies, and market perception.

This tool conducts deep-dive searches using Google's Custom Search API, segmenting the obtained data into manageable chunks for further analysis. It uses OpenAI's advanced NLP models to generate an informative report, delivering data-rich insights to your fingertips.

# Table of Contents

1. [Features](#features)
2. [Setup Instructions](#setup-instructions)
3. [Usage Instructions](#usage-instructions)
4. [Deployment Instructions](#deployment-instructions)

# Features

## Search Company Name

- You may search multiple company names by seperating the names with a comma

<a href="https://github.com/keshao728/pls-hire-me"><img src="https://imgur.com/6eKxii3.gif" title="source: imgur.com" /></a>

## Report

- Generates a report for the company's main products or services, business strategies, and market perception

<a href="https://github.com/keshao728/pls-hire-me"><img src="https://imgur.com/SntGku7.gif" title="source: imgur.com" /></a>

# Getting Started

These instructions will guide you through the process of setting up and running the application on your local machine for development and testing purposes.

## Prerequisites

Ensure you have the following installed on your local development machine:

- Python 3.8 or later
- Node.js and npm
- Flask
- React

Also, make sure to acquire API keys for OpenAI, Google APIs and Programmable Search Engine ID and store them in a `.env` file, an `.env.example` is provided at the `/app` of the project directory.

# Setup Instructions

## Backend

The backend is a Python Flask application.

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/keshao728/pls-hire-me.git
   ```

2. Navigate to the backend directory:

   ```bash
   cd app
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the local server env file, replace the key to your API keys:
   ```sh
   cp .env.example .env.local
   ```
5. Start the application:
   ```bash
    python app.py
   ```
   This will start the server on localhost:5003. The server endpoint is `/process`, which accepts POST requests.

## Frontend

The frontend is a React application.

1. Navigate into the frontend directory:
   ```bash
   cd react-app
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the application
   ```bash
    npm start
   ```
   This will start the React application and open it in your default web browser at http://localhost:3000.

# Usage Instructions

- Open your web browser and go to http://localhost:3000 (or the port you configured for your React app).
- You'll see an input field where you can enter the names of the companies you want to investigate, separated by commas.
- After entering the company names, click the 'Submit' button.
- The application will then generate a report for each company, which will include information about their main product or service, business strategy, and market perception.



# Deployment Instructions

This project consists of a frontend and a backend which are containerized using Docker. Below are the steps to build and deploy the project using Docker and Heroku.

## Requirements
* Docker installed on your machine. You can download Docker [here](https://www.docker.com/products/docker-desktop).
* Heroku CLI installed on your machine. You can download it from [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

## Steps

### Docker Setup

1. Build the Docker container

    Navigate to the project root directory and build the Docker image.

    ```bash
    docker build -t kelly-ai .
    ```

2. Run the Docker container

    Check if everything is set up correctly by running the Docker container.

    ```bash
    docker run -p 5003:5003 kelly-ai
    ```

    After running the command, you should be able to access the application at `http://localhost:5003`.

### Heroku Deployment

1. Login to Heroku

    Login to your Heroku account via the CLI.

    ```bash
    heroku login
    ```

2. Create a new Heroku app

    Create a new app on Heroku.

    ```bash
    heroku create plz-hire-me
    ```

3. Login to Heroku Container Registry

    Login to Heroku Container Registry using the CLI.

    ```bash
    heroku container:login
    ```

4. Build the Docker Image and Push to Heroku

    After logging in to the Heroku Container Registry, you can build and push your Docker image.

    ```bash
    heroku container:push web --app plz-hire-me
    ```

5. Release the image to your app

    After pushing the image to Heroku, you need to release it to deploy your app.

    ```bash
    heroku container:release web --app plz-hire-me
    ```
### Updating the container on Heroku
1. Build the Docker container

    Navigate to the project root directory and build the Docker image.

    ```bash
    docker build -t kelly-ai .
    ```

2. Tag the Docker image


    ```bash
    docker tag kelly-ai:latest registry.heroku.com/plz-hire-me/web
    ```

3. Push the Docker image

    Finally, push your Docker image to the Heroku registry.

    ```bash
    docker push registry.heroku.com/plz-hire-me/web
    ```
4. Release the image to your app

    After pushing the image to Heroku, you need to release it to deploy your app.

    ```bash
    heroku container:release web --app plz-hire-me
    ```

After completing these steps, your application should be live on Heroku!

---
Please note: This guide assumes you are using a Unix-like operating system (Linux, MacOS, WSL, etc.). If you are using Windows, please ensure you are using the correct commands for your operating system.


Note: Don't forget to secure your API keys before deploying the application to a production environment.
