import pandas as pd
import os
df=pd.read_csv('data/Video_Games_Sales_as_at_22_Dec_2016.csv')

df = df.dropna(subset=["Name", "Year_of_Release", "Global_Sales"])
df["User_Score"] = pd.to_numeric(df["User_Score"], errors="coerce")
df.columns = df.columns.str.lower().str.replace(" ", "_")

df.to_csv("data/cleaned_game_sales.csv", index=False)

print("Cleaned dataset saved as 'cleaned_game_sales.csv' in data folder")