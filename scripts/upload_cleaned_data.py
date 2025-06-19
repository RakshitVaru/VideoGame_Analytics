import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.snowflake_connector import connect_to_snowflake

# Load cleaned CSV
df = pd.read_csv("data/cleaned_game_sales.csv")

# Connect to Snowflake
conn = connect_to_snowflake()
cursor = conn.cursor()

# Create table if not exists (optional, already done in previous step)
cursor.execute("""
CREATE OR REPLACE TABLE game_sales (
    name STRING,
    platform STRING,
    year_of_release INT,
    genre STRING,
    publisher STRING,
    na_sales FLOAT,
    eu_sales FLOAT,
    jp_sales FLOAT,
    other_sales FLOAT,
    global_sales FLOAT,
    critic_score FLOAT,
    critic_count INT,
    user_score FLOAT,
    user_count INT,
    developer STRING,
    rating STRING
);
""")

# Insert rows in batch
# for _, row in df.iterrows():
#     cursor.execute("""INSERT INTO game_sales VALUES """, tuple(row))

insert_query = """
    INSERT INTO game_sales (
        name, platform, year_of_release, genre, publisher,
        na_sales, eu_sales, jp_sales, other_sales, global_sales,
        critic_score, critic_count, user_score, user_count, developer, rating
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    # Convert row to list and replace NaN with None
    row_clean = [None if pd.isna(val) else val for val in row.tolist()]
    cursor.execute(insert_query, row_clean)

# # # Insert rows in batch
# for _, row in df.iterrows():
#     cursor.execute("""
#         INSERT INTO game_sales VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("Data uploaded to Snowflake successfully!")