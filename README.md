# Gradeks

## Overview

The official school portal app (de.edu.orb.ru) launched with delays and often froze due to client-side errors (the client did not send requests to the server correctly, resulting in grades not loading). The app also did not notify users of grade changes — students had to manually check the website, missing important updates. My project completely compensated for these shortcomings by providing a stable and informative interface directly in Telegram.
## Features

- Aggregation of grades from the web-based diary using an internal identifier or login/password authentication.
- User authentication and management with secure storage of access tokens.
- Storage and caching of grade data and user profiles in a database.
- Business logic for calculating grade weight, statistics, average grade trends, and required grades for improvement.
- Notification module for instant delivery of grade updates via the Telegram Bot API.

## Install & Upgrade

```
git clone https://github.com/Ramedon1/gradeks-backend.git
```

```
cd gradeks-backend
```

```
cp .env.example .env
```

Fill in the variables

```
pip install -r requirements.txt
```

```
python run.py
```

If you want to run only Telegram bot:

```
python run_bot.py 
```

> [!IMPORTANT]  
> Don't forget to migrate Alembic

## Environment Variables

| Variable          |                                   Type                                    |
|-------------------|:-------------------------------------------------------------------------:|
| REDIS_HOST        |                             `Redis server ip`                             |
| REDIS_PORT        |                            `Redis server port`                            |
| REDIS_USER        |                              `User DB Redis`                              |
| REDIS_PASS        |                         `Password for Redis user`                         |
| POSTGRES_HOST     |                             `Database server`                             |
| POSTGRES_PORT     |                              `Database port`                              |
| POSTGRES_DB       |                              `Database user`                              |
| POSTGRES_USER     |                            `Database password`                            |
| POSTGRES_PASSWORD |                            `Database password`                            |
| BOT_TOKEN         |                            `Telegam Bot Token`                            |
| WEB_UI_URL        |                  `PATH to web (ex. https://graeks.xyz/)`                  |
| PROXY_URL         | `http proxy if need on this format: http://{user}:{password}@{ip}:{port}` |
| ADMIN_ID          |           `Telegram ID the user who will be the administrator`            |

# Gradeks Backend Endpoints

This document provides an overview of the key API endpoints found under the "web/routes" directory, describing their functionalities and typical use scenarios. Each route is associated with a specific router (FastAPI router) and may have multiple endpoint definitions.



## Endpoints

### User Endpoints
Base Path Prefix: `/user`  
Router Import: `from web.routes.users import user_router`

• POST `/user/login`  
  - Description: Validates user login data, fetches or creates a user entry by telegram_id, and returns an access token.  

• POST `/user/me`  
  - Description: Retrieves user info given a specific filter (e.g., quarters, half-year, etc.).  

• POST `/user/link`  
  - Description: Links the user’s diary ID, verifies the diary link, and calls functions to populate grade data.  

---

### Grade Endpoints
Base Path Prefix: `/grade`  
Router Import: `from web.routes.grade import grade_router`

• POST `/grade/change/{grade_type}`  
  - Description: Changes the grade display type for a user (e.g., "old" vs. "new").  

• POST `/grade/get`  
  - Description: Fetches grades based on a specified filter (e.g., current quarter, semester).  

---

### Distribution Endpoints
Base Path Prefix: `/distribution`  
Router Import: `from web.routes.distribution import distribution_router`

• POST `/distribution/activate`  
  - Description: Activates distribution (e.g., notifications or data distribution) for the current user.  

• POST `/distribution/deactivate`  
  - Description: Deactivates distribution for the current user.  

---

## Request & Response Examples

Below are brief request/response sketches for illustration (replace placeholders as needed).

```bash
# Example: user login
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "telegram_data": {
           "user": {
              "id": "123456789"
           }
        }
      }' \
  http://localhost:8000/user/login
```

```bash
# Example: get grades
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{
        "filter": "quarter"
      }' \
  http://localhost:8000/grade/get
```


## License

This project is licensed under the [MIT License](LICENSE).  
