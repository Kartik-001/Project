import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv('data.csv')

X = df.drop('MEDV', axis=1)
y = df['MEDV']

stratified_splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in stratified_splitter.split(df, df['CHAS']):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

models = [
    ('Linear Regression', LinearRegression()),
    ('Ridge Regression', Ridge()),
    ('Lasso Regression', Lasso()),
    ('Random Forest Regressor', RandomForestRegressor()),
    ('Support Vector Regressor', SVR()),
    ('DecisionTreeRegressor', DecisionTreeRegressor())
]

results = []
for name, model in models:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', model)
    ])
    
    mse_scores = -cross_val_score(pipeline, X_train, y_train, scoring='neg_mean_squared_error', cv=5)
    
    mean, std = mse_scores.mean(), mse_scores.std()
    results.append((name, mean, std))

for name, mean, std in results:
    print(f'{name}: Mean MSE = {mean}, Standard Deviation = {std}')

with open('models_output.txt', 'w') as file:
    for name, mean, std in results:
        file.write(f'{name}: Mean MSE = {mean}, Standard Deviation = {std}\n')
