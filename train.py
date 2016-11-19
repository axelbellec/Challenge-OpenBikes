import pandas as pd

from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier

from get_data import read_test_dataset


df_train = pd.read_csv('dataset_train.csv', index_col=0)
df_test = read_test_dataset()

clf = RandomForestClassifier()


def split(dataframe, target, ignored):
    ''' Split the features from the target '''
    features = [column for column in dataframe.columns if column not in [target] + [ignored]]
    X = dataframe[features]
    Y = dataframe[target]
    return X, Y


X_train, Y_train = split(dataframe=df_train, target='bikes', ignored=['spaces', 'moment', 'city'])

# # Train the regressor
# clf.fit(X_train, Y_train)

# # Split the test set into features and targets
# X_test, Y_test = split(dataframe=df_test, target='bikes', ignored='spaces')

# # Predict the outcome of the test set
# prediction = clf.predict(X_test)
