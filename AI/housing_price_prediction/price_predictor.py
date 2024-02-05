import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from joblib import dump, load

# Load the dataset
df = pd.read_csv('data.csv')

# Separate features (X) and target variable (y)
X = df.drop('MEDV', axis=1)
y = df['MEDV']

# Use StratifiedShuffleSplit for creating training and test sets
stratified_splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in stratified_splitter.split(df, df['CHAS']):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# Create a pipeline with imputation, scaling, and a random forest regressor
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Train the model using the training set
pipeline.fit(X_train, y_train)

# Make predictions on the test set
predictions = pipeline.predict(X_test)

# Evaluate the model using mean squared error (MSE)
mse = mean_squared_error(y_test, predictions)
print('Mean Squared Error: ', mse)

# Save the trained pipeline to a file
dump(pipeline, 'price_predictor.joblib')
