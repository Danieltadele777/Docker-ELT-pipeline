import os
import requests
import snowflake.connector
import time

# Fetch from API
def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    res = requests.get(url)
    data = res.json()
    timestamp = int(time.time())
    return [
        ("bitcoin", data["bitcoin"]["usd"], timestamp),
        ("ethereum", data["ethereum"]["usd"], timestamp)
    ]

# Load into Snowflake
def load_to_snowflake(data):
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            coin STRING,
            price FLOAT,
            timestamp NUMBER
        )
    """)

    insert_query = "INSERT INTO crypto_prices (coin, price, timestamp) VALUES (%s, %s, %s)"


    try:
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ Inserted {len(data)} rows into Snowflake.")
    except Exception as e:
        print(f"❌ Error inserting data: {e}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    prices = fetch_prices()
    load_to_snowflake(prices)


