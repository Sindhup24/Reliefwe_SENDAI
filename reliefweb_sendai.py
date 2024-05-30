import requests
import pandas as pd

# Define the ReliefWeb API endpoint and parameters
api_url = "https://api.reliefweb.int/v1/reports"
params = {
    'appname': 'disaster-recovery-script',
    'query[value]': 'disaster',
    'filter[field]': 'country',
    'filter[value]': 'Israel',  # Replace with the desired region
    'sort': 'date:desc',
    'limit': 30
}

# Fetch the data from the ReliefWeb API
response = requests.get(api_url, params=params)
data = response.json()

# Extract relevant data
disaster_data = []
for report in data['data']:
    fields = report['fields']
    disaster_info = {
        'Title': fields.get('title'),
        'Date': fields.get('date', {}).get('created'),
        'Source': fields.get('source', [{}])[0].get('name'),
        'Country': fields.get('country', [{}])[0].get('name'),
        'Disaster_Type': fields.get('disaster_type', [{}])[0].get('name'),
        'URL': fields.get('url')
    }
    disaster_data.append(disaster_info)

# Convert the data to a DataFrame
df = pd.DataFrame(disaster_data)

# Print the data
print("Disaster Data:")
print(df)

# Function to organize data using SENDAI framework indicators
def organize_by_sendai(df):
    sendai_indicators = {
        'A-1': 'Number of deaths, missing persons and directly affected persons attributed to disasters',
        'B-2': 'Number of countries that adopt and implement national disaster risk reduction strategies in line with the Sendai Framework',
        'C-3': 'Direct disaster economic loss in relation to global gross domestic product (GDP)',
        'D-4': 'Disaster damage to critical infrastructure and disruption of basic services',
        'E-5': 'Number of countries with national and local disaster risk reduction strategies',
        'F-6': 'Proportion of local governments that adopt and implement local disaster risk reduction strategies in line with national strategies',
        'G-7': 'Availability of and access to multi-hazard early warning systems and disaster risk information and assessments'
    }

    organized_data = {key: [] for key in sendai_indicators.keys()}

    for _, row in df.iterrows():
        organized_data['A-1'].append(row['Title'])
        organized_data['B-2'].append(row['Country'])
        organized_data['C-3'].append(row['Disaster_Type'])
        organized_data['D-4'].append(row['Source'])
        organized_data['E-5'].append(row['Date'])
        organized_data['F-6'].append(row['URL'])
        organized_data['G-7'].append(row['Title'])

    return organized_data

# Organize the data by SENDAI framework indicators
sendai_data = organize_by_sendai(df)

# Convert organized data to a DataFrame
sendai_df = pd.DataFrame(sendai_data)

# Print the organized data
print("\nOrganized Data by SENDAI Framework:")
print(sendai_df)
