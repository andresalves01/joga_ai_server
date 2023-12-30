# Joga Ai - A Soccer Court Booking App

Joga Ai (in English would be something close to "Play There") is a Flask-based backend for a soccer court booking application that allows users to find and reserve soccer courts in their region, similar to how Airbnb handles property rentals. Additionally, this backend offers a integration for court owners who wish to manage their court bookings.

This README provides an overview of the project, its features, and instructions on how to set it up and use it.

## Table of Content

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation and Usage](#installation-and-usage)
- [Tables and Objects](#tables-and-objects)
- [API Documentation](#api-documentation)
  - [Methods](#general-methods)
  - [Specific Requisitions](#specific-requisitions)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication:** Users can create accounts, log in and book soccer courts and get soccer courts recomendations.
- **Search and Filter:** Users can search for soccer courts based on location, amenities, rating, price and availability.
- **Booking Management:** Users can view, manage and delete their court bookings.
- **Reviews and Ratings:** Users can leave reviews and ratings of courts after bookings.

- **Court Creation:** Court owners can register their properties for rental.

## Getting Started

If you want to use this server without having to set up the entire environment, it is available at https://jogaai.azurewebsites.net/. The server is hosted on Azure with a free plan, which may result in the initial connection taking at least four minutes to establish. However, once connected, the program should run as expected.

Nevertheless, if you prefer to set up and run Joga Ai on your local development environment, follow the following steps.

### Prerequisites

- [Docker](https://docs.docker.com/) (optional)
- [Python 3.10](https://docs.python.org/3.10/)
- [Flask 3.0](https://flask.palletsprojects.com/en/3.0.x/)
- [Geopy 2.4](https://geopy.readthedocs.io/en/stable/)
- [Gunicorn 21.2](https://gunicorn.org/)
- [Psycopg2 2.9.9](https://www.psycopg.org/docs/install.html)
- [Unidecode 1.3.7](https://pypi.org/project/Unidecode/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

### Installation and Usage

#### Docker
If you have docker installed, you can pull this repository as a docker image and run it, without the need to individually install each dependence individually.

Pull the image:
```bash
docker pull andrealves01/joga_ai:latest
```

And then run it with:
```bash
docker run -p 5000:5000 --name joga_ai andrealves01/joga_ai
```

Now you can access it with the URL http://localhost:5000/.


#### Git Clone
If you prefer to manually install the packages, you can clone this repository using
```bash
git clone https://github.com/andresalves01/joga_ai_server.git
```

Navigate to the project folder:
```bash
cd joga_ai_server
```

Create a virtual environment:
```bash
virtualenv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```

Navigate to source folder:
```bash
cd src
```

And then you can run it with:
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

And you are all set.

## API Documentation

This backend uses JSON-based RESTful APIs to communicate with clients and associate applications. Therefore, use POST to create objects, GET to read them, PUT to update and DELETE to erase data.

The main API route for now is /search/slot. There are plenty more API routes in app.py file than this README documents right now, but further documentation will be added here as soon as possible.

### Methods
#### POST
POST requests are responded with an id and a message to indicate success or failure of the requested operation.

Example of a Court row creation:

**Post Request Body**
```json
{
  "name": "MyCourt",
  "description": "This is a text",
  "player_qty": 10, // Should be between 2 and 22
  "modality": "soccer",
  "rating": 5.0, // Will not affect object creation
  "address_id": null
}
```

**Success Response**
```json
{
  "id":1,
  "message": "Court row successfully created."
}
```
#### GET
For now, use /search/slot (no body required) to get couorts available for slot booking. 

#### PUT
TODO

#### DELETE
TODO

# TODOS
### Database
- Create Court Owner user type (1 User : N Courts);
- Implement user authentication;
- Create a table for payments (1 User : 1 Payment or N Users: N Payments) and make it connected to the slot reservation (1 Payment : 1 Slot Reservation);
- Implement cancellation policy;
- Create and implement Court Modalities - soccer, tennis, basketball and so on.
### Server
- Implement better exception treatment, the current one is poorly made.
- Separate app.py functions into other files, it is a mess right now.
- Not use foreign key on the server. Each model that references another should have a pointer to an object of the referenced class, at least in a 1:1 relationship.

