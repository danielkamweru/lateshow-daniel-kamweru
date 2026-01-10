# Late Show API

A Flask-based REST API for managing late-night talk show episodes, guests, and their appearances.

## Table of Contents

- [Project Structure](#project-structure)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
lateshow/
├── __init__.py          # Flask app factory
├── models.py            # SQLAlchemy models
├── app.py              # API routes
├── seed.py             # Database seeding
└── README.md           # This file
```

## Overview

The Late Show API provides a backend service for managing episodes of a late-night talk show, including guest appearances and ratings. Built with Flask and SQLAlchemy, it offers a clean REST API interface for frontend applications.

## Features

- Complete CRUD operations for episodes
- Guest management with occupations
- Appearance tracking with ratings (1-5 scale)
- Many-to-many relationships with cascade deletes
- Data validation and error handling
- CORS support for frontend integration
- RESTful JSON API

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd lateshow
```

2. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-migrate flask-cors sqlalchemy-serializer
```

3. Initialize the database:
```bash
python3 -c "
from __init__ import create_app, db
from models import Episode, Guest, Appearance
app = create_app()
with app.app_context():
    db.create_all()
"
```

4. Seed the database:
```bash
python3 seed.py
```

## Usage

Start the development server:
```bash
python3 app.py
```

The API will be available at `http://localhost:5555`

## API Endpoints

### Episodes

#### GET /episodes
Returns all episodes with basic information.

```bash
curl http://localhost:5555/episodes
```

Response:
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
]
```

#### GET /episodes/:id
Returns detailed episode information including appearances.

```bash
curl http://localhost:5555/episodes/1
```

Success Response (200):
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "episode_id": 1,
      "guest_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

Error Response (404):
```json
{
  "error": "Episode not found"
}
```

#### DELETE /episodes/:id
Deletes an episode and all associated appearances.

```bash
curl -X DELETE http://localhost:5555/episodes/1
```

Returns: 204 No Content

### Guests

#### GET /guests
Returns all guests.

```bash
curl http://localhost:5555/guests
```

Response:
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
]
```

### Appearances

#### POST /appearances
Creates a new guest appearance on an episode.

```bash
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "episode_id": 1,
    "guest_id": 2
  }'
```

Request Body:
```json
{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 2
}
```

Success Response (201):
```json
{
  "id": 5,
  "rating": 5,
  "episode_id": 1,
  "guest_id": 2,
  "episode": {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  "guest": {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "comedian"
  }
}
```

Error Response (400):
```json
{
  "errors": ["validation errors"]
}
```

### Validation Rules

- `rating`: Integer between 1-5 (inclusive)
- `episode_id`: Must reference existing episode
- `guest_id`: Must reference existing guest

## Database Schema

### Models

**Episode**
- `id` (Integer, Primary Key): Unique episode identifier
- `date` (String, Required): Episode air date
- `number` (Integer, Required): Episode number in series

**Guest**
- `id` (Integer, Primary Key): Unique guest identifier
- `name` (String, Required): Guest full name
- `occupation` (String, Required): Guest profession/occupation

**Appearance**
- `id` (Integer, Primary Key): Unique appearance identifier
- `rating` (Integer, Required): Performance rating (1-5 scale)
- `episode_id` (Integer, Foreign Key): Reference to Episode
- `guest_id` (Integer, Foreign Key): Reference to Guest

### Relationships

- Episodes have many Guests through Appearances
- Guests have many Episodes through Appearances
- Appearances belong to both Episode and Guest
- Cascade deletes: Removing an Episode or Guest removes associated Appearances

## Testing

Test the API endpoints:

```bash
# Get all episodes
curl http://localhost:5555/episodes

# Get specific episode
curl http://localhost:5555/episodes/1

# Get all guests
curl http://localhost:5555/guests

# Create appearance
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{"rating": 4, "episode_id": 1, "guest_id": 1}'

# Test validation (invalid rating)
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{"rating": 6, "episode_id": 1, "guest_id": 1}'

# Delete episode
curl -X DELETE http://localhost:5555/episodes/1
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

MIT License

Copyright (c) 2024 Late Show API Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
