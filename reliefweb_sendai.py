import requests
import pandas as pd

# Function to fetch disaster data from the ReliefWeb API
def fetch_disaster_data(disaster_type, country=None):
    api_url = "https://api.reliefweb.int/v1/disasters?appname=rw-user-0&profile=list&preset=latest&slim=1&query%5Bvalue%5D=%28Cyclone%29+AND+%28country.id%3A119+AND+type.id%3A4611%29&query%5Boperator%5D=AND"
    params = {
        'appname': 'disaster-recovery-script',
        'query[value]': disaster_type,
        'query[operator]': 'AND',
        'filter[field]': 'country' if country else None,
        'filter[value]': country if country else None,
        'sort': 'date:desc',
        'limit': 4  # Increase limit to fetch more data
    }

    print(f"Fetching data for {disaster_type} in {country if country else 'all countries'}...")
    response = requests.get(api_url, params={k: v for k, v in params.items() if v})
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return pd.DataFrame()

    data = response.json()

    if 'data' not in data or len(data['data']) == 0:
        print(f"No data returned for {disaster_type} in {country if country else 'all countries'}.")
        return pd.DataFrame()

    disaster_data = []
    for disaster in data['data']:
        fields = disaster.get('fields', {})
        disaster_info = {
            'Title': fields.get('name', 'N/A'),
            'Date': fields.get('date', {}).get('created', 'N/A'),
            'Source': fields.get('source', [{'name': 'N/A'}])[0].get('name', 'N/A'),
            'Country': fields.get('country', [{'name': 'N/A'}])[0].get('name', 'N/A'),
            'Disaster_Type': fields.get('type', [{'name': 'N/A'}])[0].get('name', 'N/A'),
            'URL': fields.get('url', 'N/A')
        }
        disaster_data.append(disaster_info)
    
    return pd.DataFrame(disaster_data)

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

    return pd.DataFrame(organized_data)

# Function to filter data by multiple countries
def filter_by_countries(df, country_list):
    return df[df['Country'].isin(country_list)]

# Main function to fetch, process, and display data
def main():
    disaster_types = ['Cyclone', 'Earthquake', 'Flood']
    country_list = ['Bangladesh', 'Madagascar']

    all_disaster_data = pd.DataFrame()
    for disaster_type in disaster_types:
        disaster_data = fetch_disaster_data(disaster_type)
        if not disaster_data.empty:
            all_disaster_data = pd.concat([all_disaster_data, disaster_data], ignore_index=True)

    if all_disaster_data.empty:
        print("No disaster data found for the specified types.")
        return

    sendai_data = organize_by_sendai(all_disaster_data)
    filtered_data = filter_by_countries(all_disaster_data, country_list)

    print("All Disaster Data:")
    print(all_disaster_data)
    
    print("\nOrganized Data by SENDAI Framework:")
    print(sendai_data)

    print("\nFiltered Data by Countries:")
    print(filtered_data)

# Uncomment the following line to run the main function when executing the script
main()
