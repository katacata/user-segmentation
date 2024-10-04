import pandas as pd
from datetime import datetime, date

# Read CSV files
df1 = pd.read_csv('csv1.csv')  # Contains name, mobile, email
df2 = pd.read_csv('csv2.csv')  # Contains year of birth

# Merge DataFrames based on 'name'
merged_df = pd.merge(df1, df2, on='name')

# Calculate age
def calculate_age(year_of_birth):
    current_year = date.today().year
    return current_year - year_of_birth

merged_df['Age'] = merged_df['Year_of_Birth'].apply(calculate_age)

# Create final DataFrame with required columns
final_df = merged_df[['name', 'mobile', 'email', 'Age']]

# Save result to a new CSV file
final_df.to_csv('output.csv', index=False)

print("CSV merging and age calculation completed. Result saved to output.csv")
