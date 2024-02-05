from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('data.csv')

X = df.drop('MEDV', axis=1)
y = df['MEDV']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print('---------------------------------------------------------')

# Feature Importance from Models
model = RandomForestRegressor()
model.fit(X_train, y_train)
feature_importances = model.feature_importances_
print(feature_importances)

print('---------------------------------------------------------')

# Correlation Analysis
correlation_matrix = df.corr()
correlation_with_target = correlation_matrix['MEDV'].abs().sort_values(ascending=False)
print(correlation_with_target)

print('---------------------------------------------------------')

# Recursive Feature Elimination (RFE)
from sklearn.feature_selection import RFE

model = RandomForestRegressor()
rfe = RFE(model, n_features_to_select=1)
fit = rfe.fit(X_train, y_train)
selected_features = X.columns[fit.support_]
print("Selected Features:", selected_features)

print('---------------------------------------------------------')

# SelectKBest
from sklearn.feature_selection import SelectKBest, f_regression

selector = SelectKBest(score_func=f_regression, k=5)
X_new = selector.fit_transform(X_train, y_train)
print(X_new)

print('---------------------------------------------------------')

# LASSO Regression (L1 Regularization)

from sklearn.linear_model import Lasso

model = Lasso(alpha=0.01)
model.fit(X_train, y_train)
feature_coefficients = pd.Series(model.coef_, index=X.columns)
print("Feature Coefficients:")
print(feature_coefficients)

print('---------------------------------------------------------')
