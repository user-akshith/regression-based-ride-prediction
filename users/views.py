from django.shortcuts import render

# Create your views here.
from ast import alias
from concurrent.futures import process
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages


from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import datetime as dt
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import classification_report


# Create your views here.

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(
                loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})



def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

def DatasetView(request):
    path = settings.MEDIA_ROOT + "//" + 'uber_ride_fare_dataset.csv'
    df = pd.read_csv(path)
    df = df.to_html
    return render(request, 'users/viewdataset.html', {'data': df})


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

from .forms import PredictionForm

media_path = "media/"
model_path = os.path.join(media_path, "gbr_model.pkl")
scaler_path = os.path.join(media_path, "scaler.pkl")

def training(request):
    context = {}

    # Path to your fixed dataset inside your project
    dataset_path = os.path.join(media_path, "uber_ride_fare_dataset.csv")

    if request.method == "GET":
        # Load CSV directly from path
        df = pd.read_csv(dataset_path)

        # Preprocessing
        df_encoded = pd.get_dummies(df, columns=['time_of_day', 'day_of_week', 'weather', 'moon_phase'], drop_first=True)
        df_encoded.drop(columns=['ride_id'], inplace=True)

        X = df_encoded.drop(columns=['fare_amount'])
        y = df_encoded['fare_amount']

        # Normalize
        scaler = StandardScaler()
        X[['distance_km', 'hour_of_day', 'uv_index', 'fare_per_km']] = scaler.fit_transform(
            X[['distance_km', 'hour_of_day', 'uv_index', 'fare_per_km']]
        )
        joblib.dump(scaler, scaler_path)

        # Train-Test Split and Model Training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42)
        gbr.fit(X_train, y_train)
        joblib.dump(gbr, model_path)

        # Evaluation
        y_pred = gbr.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        context['mse'] = round(mse, 2)
        context['r2'] = round(r2 * 100, 2)

        # Plot 1: Feature Importance
        importances = gbr.feature_importances_
        features = X.columns
        indices = np.argsort(importances)[::-1]

        plt.figure(figsize=(10, 5))
        sns.barplot(x=importances[indices], y=features[indices])
        plt.title('Feature Importance')
        plt.tight_layout()
        feat_path = os.path.join(media_path, 'feature_importance.png')
        plt.savefig(feat_path)
        context['feat_plot'] = feat_path

        # Plot 2: Actual vs Predicted
        plt.figure(figsize=(6, 5))
        plt.scatter(y_test, y_pred, alpha=0.7)
        plt.xlabel("Actual Fare")
        plt.ylabel("Predicted Fare")
        plt.title("Actual vs Predicted Fare")
        plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
        plt.tight_layout()
        pred_path = os.path.join(media_path, 'prediction_plot.png')
        plt.savefig(pred_path)
        context['pred_plot'] = pred_path


    return render(request, 'users/training.html', context)


def prediction(request):
    form = PredictionForm()
    fare = None

    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['fare_per_km'] = data['distance_km'] * 0.25
            input_df = pd.DataFrame([data])

            df_encoded = pd.get_dummies(input_df)
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)

            original_cols = model.feature_names_in_
            for col in original_cols:
                if col not in df_encoded.columns:
                    df_encoded[col] = 0
            df_encoded = df_encoded[original_cols]

            df_encoded[['distance_km', 'hour_of_day', 'uv_index', 'fare_per_km']] = scaler.transform(
                df_encoded[['distance_km', 'hour_of_day', 'uv_index', 'fare_per_km']]
            )

            fare = round(model.predict(df_encoded)[0], 2)

    return render(request, 'users/predictForm.html', {'form': form, 'fare': fare})
