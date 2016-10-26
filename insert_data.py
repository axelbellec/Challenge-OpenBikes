import os

import click
import pandas as pd
from sqlalchemy.orm import sessionmaker

from models import engine, City, Station, BikeTerminal, Weather, Coordinates


def remove_file_extension(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def insert_city(city):
    ''' Insert a city into SQL Database. '''

    click.secho('Inserting {} in db.cities'.format(city), fg='cyan')
    db.add(City(name=city))
    db.commit()


def insert_stations(city):
    ''' Insert all stations for a city into SQL Database. '''

    click.secho('Inserting {} in db.stations'.format(city), fg='cyan')
    directory_files = os.path.join(data_directory, city)
    if os.path.isdir(directory_files):
        for station in os.listdir(os.path.join(directory_files, 'stations')):
            if station.endswith('.csv'):
                city_obj = db.query(City).filter(City.name == city).one()
                db.add(Station(name=remove_file_extension(station), city_id=city_obj.id))
        db.commit()


def insert_coordinates(city):
    ''' Insert all stations coordinates for a city into SQL Database. '''

    click.secho('Inserting {} in db.coordinates'.format(city), fg='cyan')
    directory_files = os.path.join(data_directory, city)
    if os.path.isdir(directory_files):
        coord = pd.read_csv(os.path.join(directory_files, 'coordinates.csv'), sep=',')
        for index, row in coord.iterrows():
            try:  # there are more coordinates than stations
                station_obj = db.query(Station).filter(Station.name == row['station']).one()
                db.add(Coordinates(station_id=station_obj.id,
                                   altitude=row['altitude'],
                                   longitude=row['longitude'],
                                   latitude=row['latitude']))
            except:
                pass
        db.commit()


def insert_weather_moments(city):
    ''' Insert all weather metadata for a city into SQL Database. '''

    click.secho('Inserting {} in db.weather'.format(city), fg='cyan')
    directory_files = os.path.join(data_directory, city)
    if os.path.isdir(directory_files):
        weather = pd.read_csv(os.path.join(directory_files, 'weather.csv'), sep=',')
        weather['moment'] = pd.to_datetime(weather['moment'])
        for index, row in weather.iterrows():
            city_obj = db.query(City).filter(City.name == city).one()
            db.add(Weather(moment=row['moment'],
                           city_id=city_obj.id,
                           clouds=row['clouds'],
                           description=row['description'],
                           humidity=row['humidity'],
                           pressure=row['pressure'],
                           temperature=row['temperature'],
                           wind=row['wind']))
        db.commit()


def insert_bikes_and_places():
    ''' Insert all bikes and places data for a city into SQL Database. '''

    click.secho('Inserting {} in db.slots'.format(city), fg='cyan')
    directory_files = os.path.join(data_directory, city)
    if os.path.isdir(directory_files):
        for station in os.listdir(os.path.join(directory_files, 'stations')):
            if station.endswith('.csv'):
                data = pd.read_csv(os.path.join(directory_files, 'stations', station), sep=',')
                data['moment'] = pd.to_datetime(data['moment'])
                for index, row in data.iterrows():
                    city_obj = db.query(City).filter(City.name == city).one()
                    station_obj = db.query(Station).filter(Station.name == remove_file_extension(
                        station) and Station.city_id == city_obj.id).one()
                    db.add(BikeTerminal(moment=row['moment'],
                                        station_id=station_obj.id,
                                        bikes=row['bikes'],
                                        spaces=row['spaces']))
        db.commit()


def main():
    ''' Main function to compute data cleaning. '''

    DBSession = sessionmaker(bind=engine)
    db = DBSession()

    current_directory = os.getcwd()
    data_directory = os.path.join(current_directory, 'data')

    CITIES = ['toulouse', 'lyon', 'paris']

    for city in CITIES:
        insert_city(city)
        insert_stations(city)
        insert_coordinates(city)
        insert_weather_moments(city)
        insert_bikes_and_places()

    db.close()

if __name__ == '__main__':
    main()
