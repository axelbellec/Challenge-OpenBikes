import numpy as np
import pandas as pd

from sklearn import model_selection, metrics
from sklearn.ensemble import RandomForestRegressor

from get_data import read_test_dataset, add_weather_updates, extract_time_features


df_train = pd.read_csv('dataset_train.csv', index_col=0)
df_test = read_test_dataset()

clf = RandomForestRegressor()


def split(dataframe, target, ignored):
    ''' Split the features from the target '''
    features = [column for column in dataframe.columns if column not in [target] + ignored]
    X = dataframe[features]
    Y = dataframe[target].ravel()
    return X, Y


weather_var = ['description']
station_metadata = ['altitude', 'latitude', 'longitude', 'station']

stations = (station for station in df_train.station.unique() if str(station) != 'nan')
for station in stations:
    # Filter rows on station name
    df_train_station = df_train[df_train.station == station]

    # Load only the last 30 days
    df_train_station.set_index(pd.to_datetime(df_train_station['moment']), inplace=True)
    del df_train_station['moment']
    index_from = df_train_station.index.max()
    index_to = index_from - pd.Timedelta('30 days')
    df_train_station = df_train_station[
        (df_train_station.index >= index_to) & (df_train_station.index < index_from)
    ].copy()
    df_train_station.reset_index(inplace=True)

    # Split the train set into features and targets
    X, y = split(
        dataframe=df_train_station,
        target='bikes',
        ignored=['spaces', 'moment', 'city'] + weather_var + station_metadata
    )

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X.values, y, test_size=0.2)

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    score = metrics.mean_absolute_error(y_test, y_pred)
    print(station, score)

# Plot it using pandas.Series

# # Train the regressor
# clf.fit(X_train, Y_train)

# # Filter rows on station name
# df_test_station = df_test[df_test.station == station]
# # Fill NaN values
# df_test_station.fillna(value=.0, axis=1, inplace=True)
# # Add weather updates
# df_test_station = add_weather_updates(df_test_station, city)
# # Then add time features
# extract_time_features(df_test_station)

# # Split the test set into features and targets
# X_test, Y_test = split(
#     dataframe=df_test_station,
#     target='bikes',
#     ignored=['spaces', 'moment', 'city'] + weather_var + station_metadata
# )

# # Predict the outcome of the test set
# prediction = clf.predict(X_test)

# # Compute the mean absolute error
# score = np.mean(abs(Y_test - prediction))
