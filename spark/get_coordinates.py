import requests
import json
import csv

if __name__ == "__main__":
    with open('Datasets/all_cities_census.txt') as f:
        content = f.readlines()

    cities = [x.strip() for x in content]

    with open('Datasets/cities.csv', mode='w') as csv_file:
        fieldnames = ['City', 'State', 'Abbreviation','coordinates','crime_index','traffic_index','pollution_index','health_care_index','rent_index','property_price_to_income_ratio','safety_index','cpi_index']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for city in cities:
            print("Getting coordinates and indices for "+city)
            city_name = city.split(',')[0]
            state_name = city.split(',')[1]
            state_code = city.split(',')[2]

            coord = None
            response = requests.get('https://nominatim.openstreetmap.org/search.php?q='+city_name+", "+state_name+'&polygon_geojson=1&format=json')
            if response:
                data = response.json()
                try:
                    coord = data[0]['geojson']['coordinates']
                except:
                    coord = []

            response = requests.get('http://www.numbeo.com/api/indices?api_key=ycpmuzwqm08144&query='+city_name +", "+state_code, allow_redirects=True)
            crime_index = None
            traffic_index = None
            pollution_index = None
            health_care_index = None
            rent_index = None
            property_price_to_income_ratio = None
            safety_index = None
            cpi_index = None
            if response:
                data = response.json()
                if 'crime_index' in data:
                    crime_index = data['crime_index']
                if 'traffic_index' in data:   
                    traffic_index = data['traffic_index'] or ''
                if 'pollution_index' in data:
                    pollution_index = data['pollution_index'] or ''
                if 'health_care_index' in data:
                    health_care_index = data['health_care_index'] or ''
                if 'rent_index' in data:
                    rent_index = data['rent_index'] or ''
                if 'property_price_to_income_ratio' in data:
                    property_price_to_income_ratio = data['property_price_to_income_ratio'] or ''
                if 'safety_index' in data:
                    safety_index = data['safety_index']
                if 'cpi_index' in data:
                    cpi_index = data['cpi_index']

            writer.writerow({'City': city_name, 'State': state_name, 'Abbreviation':state_code,'coordinates':coord,'crime_index':crime_index,
            'traffic_index':traffic_index,
            'pollution_index':pollution_index,
            'health_care_index':health_care_index,
            'rent_index':rent_index,'property_price_to_income_ratio':property_price_to_income_ratio,'safety_index':safety_index,'cpi_index':cpi_index})

    print("********** done ***********")