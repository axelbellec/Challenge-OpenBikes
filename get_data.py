import click
import numpy as np
import pandas as pd


def get_station_updates(city, station):
    df = pd.read_csv('data/{}/stations/{}.csv'.format(city, station), sep=',')
    df['moment'] = pd.to_datetime(df['moment'])
    return df.assign(station=station, city=city)


def get_weather_updates(city):
    df = pd.read_csv('data/{}/weather.csv'.format(city))
    df['moment'] = pd.to_datetime(df['moment'])
    return df


def extract_time_features(df):
    df['weekday'] = df['moment'].apply(lambda m: m.weekday())
    df['hour'] = df['moment'].apply(lambda m: m.hour)
    df['minute'] = df['moment'].apply(lambda m: m.minute)


def add_weather_updates(city_df, city_name):
    weather_df = get_weather_updates(city_name)
    city_df.index = np.searchsorted(weather_df['moment'], city_df['moment'])
    joined_df = pd.merge(left=city_df, right=weather_df,
                         left_index=True, right_index=True, how='right')
    joined_df.rename(columns={'moment_x': 'moment', 'moment_y': 'moment_weather'}, inplace=True)
    del joined_df['moment_weather']
    return joined_df


def add_station_coordinates(city_df, city_name):
    coord = pd.read_csv('data/{}/coordinates.csv'.format(city_name))
    joined_df = pd.merge(left=city_df, right=coord, on='station', how='left')
    return joined_df


def read_test_dataset():
    to_predict_df = pd.read_csv('data/test-blank.csv', index_col=0)
    to_predict_df['moment'] = pd.to_datetime(to_predict_df.index)
    extract_time_features(to_predict_df)
    return to_predict_df


def main():
    test_df = read_test_dataset()
    city_stations = pd.unique(test_df[['city', 'station']].values)

    df = pd.DataFrame()
    for city, station in city_stations:
        click.secho('Getting stations data for '.format(city), fg='cyan')
        print(city, station)
        df = df.append(get_station_updates(city, station))

    dataset = pd.DataFrame()
    for city in pd.unique(test_df['city']):
        city_df = df[df['city'] == city]
        df_tmp_weather = add_weather_updates(city_df, city)
        df_tmp_coord = add_station_coordinates(df_tmp_weather, city)
        dataset = dataset.append(df_tmp_coord)

    extract_time_features(dataset)
    dataset.to_csv('dataset_train.csv')

if __name__ == '__main__':
    main()
