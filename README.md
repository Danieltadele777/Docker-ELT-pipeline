# Pipeline with Docker + Snowflake

This project demonstrates a production-style **ETL (Extract, Transform, Load)** pipeline using Docker, Python, and Snowflake. It fetches live crypto prices using the [CoinGecko API](https://www.coingecko.com/), containers the pipeline using Docker, and loads it into a Snowflake table.

---
## Table of contents
 - [Overview](#overview)
 - [Project Structure](#project-structure)
 - [How It Works](#how-it-works)
 - [Final Outcome](#final-outcome)
 - [Environment Variables](#environment-variables)
 - [Skills Demonstrated](#skills-demonstrated)
 - [Screenshot](#screenshot)


## 📌 Overview

- **Extract**: Bitcoin & Ethereum prices from CoinGecko
- **Load**: Snowflake cloud data warehouse
- **Orchestrate**: Docker container
- **Tools**: Python, Snowflake Connector, Docker, `.env` file for credentials

---

## 📂 Project Structure
```

├── etl/
│ ├── Dockerfile
│ ├── run_etl.py
├── .env # Snowflake credentials
├── docker-compose.yml
└── README.md

```


---

## ⚙️ How It Works

### 1. **ETL Script** (`run_etl.py`)

- Uses `requests` to call the CoinGecko API
- Collects Bitcoin and Ethereum USD prices with a timestamp
- Connects to Snowflake using `snowflake-connector-python`
- Creates a `crypto_prices` table (if not exists)
- Inserts the data

```python

[
  ("bitcoin", 30000, 1755252841),
  ("ethereum", 3007.07, 1755252841)
]

```
### 2. **Dockerfile** 

```
FROM python:3.10-slim
WORKDIR /app
COPY run_etl.py .
RUN pip install requests snowflake-connector-python
CMD ["python", "run_etl.py"]
```

### 3. **docker-compose.yml** 

```
services:
  etl:
    build: ./etl
    env_file:
      - .env

```
### 4. **Final Outcome**  
Data is successfully written to the Snowflake ANALYTICS.ROW_DATA.CRYPTO_PRICES table:

```

| coin     | price     | timestamp   |
|----------|-----------|-------------|
| bitcoin  | 30000.0   | 1234567890  |
| bitcoin  | 119998.0  | 1755252841  |
| ethereum | 3007.07   | 1755252841  |

```


### 5. **Environment Variables** 

```
SNOWFLAKE_ACCOUNT=************
SNOWFLAKE_USER=***************
SNOWFLAKE_PASSWORD=************
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=ROW_DATA
SNOWFLAKE_WAREHOUSE=COMPUTE_WH

```

### 6. **Skills Demonstrated** 

Python scripting for ETL

Docker containerization

Working with external APIs

Snowflake cloud data warehouse integration

Using .env securely in production

### 7. **Screenshot** 

<img width="1462" height="796" alt="Docker" src="https://github.com/user-attachments/assets/fea82330-2a8f-45e3-b7c3-e5a98ffca030" />

