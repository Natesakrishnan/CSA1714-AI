
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

X = np.array([[1], [2], [3], [4], [5],
              [6], [7], [8], [9], [10]])

y = np.array([2, 4, 6, 8, 10,
              12, 14, 16, 18, 20])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)
print("Actual Values:", y_test)
print("Predicted Values:", y_pred)

print("Mean Squared Error:",
      mean_squared_error(y_test, y_pred))

print("R2 Score:", r2_score(y_test, y_pred))

new_value = np.array([[11]])
prediction = model.predict(new_value)

print("Prediction for X=11:", prediction[0])
