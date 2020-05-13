import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from numbers import Number
import network


def init_dataset(rs, filename="diabetes.csv"):

    df = pd.read_csv(filename)
    df['Glucose'] = df['Glucose'].replace(0, np.nan)
    df['BloodPressure'] = df['BloodPressure'].replace(0, np.nan)
    df['SkinThickness'] = df['SkinThickness'].replace(0, np.nan)
    df['Insulin'] = df['Insulin'].replace(0, np.nan)
    df['BMI'] = df['BMI'].replace(0, np.nan)

    df['Glucose'] = df['Glucose'].fillna(df['Glucose'].mean())
    df['BloodPressure'] = df['BloodPressure'].fillna(
        df['BloodPressure'].mean())
    df['SkinThickness'] = df['SkinThickness'].fillna(
        df['SkinThickness'].mean())
    df['Insulin'] = df['Insulin'].fillna(df['Insulin'].mean())
    df['BMI'] = df['BMI'].fillna(df['BMI'].mean())

    df_scaled = preprocessing.scale(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    df_scaled['Outcome'] = df['Outcome']

    df = df_scaled
    # print(df.describe().loc[['mean', 'std', 'min', 'max'],].round(2).abs())

    X = df.loc[:, df.columns != 'Outcome']
    y = df.loc[:, 'Outcome']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=rs)
    training_data = [(np.reshape(x, (len(x), 1)), np.reshape(
        np.array(y), (1, 1))) for x, y in zip(np.array(X_train), y_train)]
    testing_data = [(np.reshape(x, (len(x), 1)), np.reshape(
        np.array(y), (1, 1))) for x, y in zip(np.array(X_test), y_test)]

    return training_data, testing_data, X_test, y_test, X_train, y_train


def get_accuracy(net, X_val, y_val):

    validation_data = [np.reshape(x, (len(x), 1)) for x in np.array(X_val)]
    rdata = range(len(validation_data))
    n = len(validation_data)
    accuracy = 100 - \
        ((int(sum([abs(np.round(net.predict(validation_data[i])) -
                       y_val.iloc[i]) for i in rdata])) / n) * 100)
    return accuracy


def analyze_results(results):
    n_simulations, n_edges, n_periods = np.shape(results)
    mean_accuracy = [[] for i in range(n_edges)]

    for e in range(n_edges):
        for t in range(n_periods):
            mean_accuracy[e].append(
                *[np.mean([results[s][e][t] for s in range(n_simulations)])])
    return mean_accuracy


def toInt(item, precision=1e12):
    if isinstance(item, list):
        return [toInt(x) for x in item]
    else:
        return int(item * precision)


def toFloat(item, precision=1e12):
    if isinstance(item, list):
        return [toFloat(x) for x in item]
    else:
        return float(int(item) / precision)


def toList(item):

    if isinstance(item, list) or isinstance(item, tuple):
        return [toList(x) for x in item]
    elif isinstance(item, np.ndarray):
        return toList(item.tolist())
    elif isinstance(item, Number):
        return item


def toNpArray(item):

    return [np.array(x) for x in item]
