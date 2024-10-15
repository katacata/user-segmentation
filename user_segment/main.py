import pandas as pd
from datetime import datetime, date
import os
import re

def process_directory(directory_path):
    print(f"\nProcessing directory: {directory_path}")
    csv_files = sorted([file for file in os.listdir(directory_path) if file.endswith('.csv')])
    df1 = pd.read_csv(os.path.join(directory_path, csv_files[0]),  on_bad_lines='skip')
    df2 = pd.read_csv(os.path.join(directory_path, csv_files[1]),  on_bad_lines='skip')
    event_name =  directory_path.split('/')[-1]

    df2 = df2.drop_duplicates(subset=['record_id', 'meta_key'], keep='first')
    df2 = df2.pivot(index='record_id', columns='meta_key', values='meta_value')
    df2.reset_index(inplace=True)
    df2 = df2.rename(columns={'record_id': 'id'})

    df1['id'] = df1['id'].astype(str)
    df2['id'] = df2['id'].astype(str)

    merged_df = pd.merge(df1, df2, on='id', how='outer')

    required_columns = ['name', 'mobile', 'email', 'birth', 'age', 'byear', 'bmonth', 'work', 'gender', 'marriage', 'title']
    target_columns = []
    for column in required_columns:
        if column in merged_df:
            target_columns.append(column)
    final_df = merged_df[target_columns]
    final_df['event'] = event_name
    return final_df

def getSheMember():
    she_member = pd.read_csv('data/SheMember.csv',  on_bad_lines='skip')
    she_member.rename(columns={'birth_month': 'bmonth', 'birth_year': 'byear', 'phone': 'mobile'}, inplace=True)
    she_member['name'] = she_member['first_name'] + ' ' + she_member['last_name']
    return she_member[['name', 'mobile', 'email', 'byear', 'bmonth', 'gender']]

def main():
    result = []
    parent_directory = 'data'
    subdirectories = [os.path.join(parent_directory, d)
        for d in os.listdir(parent_directory)
        if os.path.isdir(os.path.join(parent_directory, d))]
    for subdir in subdirectories:
        result.append(process_directory(subdir))
    combined = pd.concat(result, ignore_index=True)
    combined['age'] = combined['age'].str.replace(r'[^\d\-,]', '', regex=True)
    def calculate_midpoint(value, offset = 2):
        match = re.match(r'^(\d+)-(\d+)$', str(value))
        if match:
            start, end = map(int, match.groups())
            return  datetime.now().year - ((start + end) // 2 + offset)
        match = re.match(r'^(\d+)$', str(value))
        if match:
            return  datetime.now().year - int(value)
        return value
    combined['age'] = combined['age'].apply(calculate_midpoint)

    def map_title(title):
        title_map = {
            'MS': 'F',
            '小姐': 'F',
            '太太': 'F',
            'MR': 'M',
            '先生': 'M',
            'MRS': 'F'
        }
        return title_map.get(title, title)
    combined['title'] = combined['title'].map(map_title)

    combined.to_csv('campaign_data.csv', index=False)
    she_member = getSheMember()
    combined = pd.concat([combined, she_member], ignore_index=True)
#     combined = combined.groupby('email').first().reset_index()
    combined.to_csv('combined_data.csv', index=False)
    print(combined)
#     combined = result[0]
#     print(result[1])
#
#     for i in range(1, len(result)):
#         combined = pd.merge(combined, result[i], on='mobile', how='outer')
#     print(combined)

if __name__ == "__main__":
    main()