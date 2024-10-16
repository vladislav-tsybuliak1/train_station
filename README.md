# Train Station API Service

The **Train Station API Service** is a Django-based project for managing train stations, trips, crew, trains, routes, and tickets. It allows users to book tickets and schedule trips.

## Installing

### Prerequisites

- Python 3.8+
- Install PostgreSQL and create db
- Docker

### Steps to Install Locally

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/vladislav-tsybuliak1/train-station-api-service.git
    cd train-station-api
    ```

2. **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
4. **Create .env file and set up environment variables**:

    ```bash
    POSTGRES_PASSWORD=<your db password>
    POSTGRES_USER=<your db user>
    POSTGRES_DB=<your db>
    POSTGRES_HOST=<your db host>
    POSTGRES_PORT=5432
    PG_DATA=/var/lib/postgresql/data
    SECRET_KEY=<your Django secret key>
    ```

5. **Run Migrations**:

    ```bash
    python manage.py migrate
    ```
6. **(Optional) Load data to db**:

    ```bash
    python manage.py loaddata train_station_db_data.json
    ```

7. **Create a Superuser.**:

    ```bash
    python manage.py createsuperuser
    ```

8. **Start the Server**:

    ```bash
    python manage.py runserver
    ```

*Note*: you can a use superuser from fixture with `admin@gmail.com` and `test123test`

## Run with Docker

### Steps to Run Using Docker

1. **Build the Docker Image**:

    ```bash
    docker-compose build
    ```

2. **Start the Services**:

    ```bash
    docker-compose up
    ```

3. **Access the API**:

    - The API will be available at `http://localhost:8000/`.

## Getting Access

To access endpoints of you don't have an account, register first here:
`api/v1/user/register/`.
If you have an account, receive you token here:
`api/v1/user/token/`.
Use your *access* token to access API endpoints.

### API Endpoints

Here are some key API endpoints you can access:

- **Stations**:
  - `GET /api/v1/stations/` - List all stations
  - `POST /api/v1/stations/` - Create a new station

- **Routes**:
  - `GET /api/v1/routes/` - List all routes
  - `POST /api/v1/routes/` - Create a new route

- **Trains**:
  - `GET /api/v1/trains/` - List all trains
  - `POST /api/v1/trains/` - Create a new train

- **Trips**:
  - `GET /api/v1/trips/` - List available journeys
  - `POST /api/v1/trips/` - Create a new journey

- **Orders**:
  - `GET /api/v1/orders/` - List all orders for current user
  - `POST /api/v1/orders/` - Create a new order

To see all the endpoints documentation with possible responses and examples go to:

- **Swagger documentation**: `http://localhost:8000/api/v1/doc/swagger/`

To access the admin panel for managing models go to:

- **Admin Panel**: `http://localhost:8000/admin/`

Use the credentials from the superuser created earlier to log in.

## Features

- **Station Management**: Add, view, update, and delete station information (name, latitude, longitude).
- **Train Management**: Manage trains with fields such as `cargo_num`, `places_in_cargo`, and `train_type`.
- **Route Management**: Create routes linking stations and calculating distances.
- **Trip Management**: Schedule trips, linking routes and trains.
- **Ticket Booking**: Book tickets for available trips.
- **Crew Management**: Assign crew members to trains.
- **Order System**: Manage orders tied to ticket purchases.
- **Pagination**: Built-in pagination for efficient data retrieval.
- **JWT Authentication**
- **Swagger documentation**
- **Filtering models by different parameters**

## Contact
For any inquiries, please contact [vladislav.tsybuliak@gmail.com](mailto:vladislav.tsybuliak@gmail.com).
