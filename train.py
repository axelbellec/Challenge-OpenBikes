import pandas as pd

from sklearn.tree import DecisionTreeClassifier

from get_data import read_test_dataset

df_train = pd.read_csv('dataset_train.csv')
df_test = read_test_dataset()

clf = DecisionTreeClassifier()


def split(dataframe, target, ignored):
    ''' Split the features from the target '''
    features = [column for column in dataframe.columns if column not in [target] + [ignored]]
    X = dataframe[features]
    Y = dataframe[target].ravel()
    return X, Y


# X_train, Y_train = split(dataframe=df_train, target='bikes', ignored='spaces')

# # Train the regressor
# clf.fit(X_train, Y_train)

# # Split the test set into features and targets
# X_test, Y_test = split(dataframe=df_test, target='bikes', ignored='spaces')

# # Predict the outcome of the test set
# prediction = regressor.predict(X_test)
