import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix, mean_absolute_error, mean_squared_error, precision_score, recall_score, accuracy_score
from category_encoders import TargetEncoder
import inotify
import json
import pickle


def train_file():
    # Variables to store values pulled from settings screen in UI
    train_file = "C:/Users/brody/OneDrive/Desktop/Capstone Project/UNSW_NB15_training-set.csv"
    n_estimators_val = 450
    max_features_val = 2
    random_state_val = 3
    max_depth_val = 4
    min_samples_leaf_val = 75

    train = pd.read_csv(train_file)

    encoder = TargetEncoder(cols=['proto', 'service', 'state'], smoothing=1.0)
    train[['proto', 'service', 'state']] = encoder.fit_transform(train[['proto', 'service', 'state']], train['label'])

    X_train = train.iloc[:, 1:15].values
    y_train = train.iloc[:, 15].values

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)

    forest = RandomForestClassifier(n_estimators = n_estimators_val, max_features = max_features_val, random_state = random_state_val, max_depth = max_depth_val, min_samples_leaf = min_samples_leaf_val)
    forest.fit(X_train, y_train)

    model_file = 'traffic_model.pkl'
    pickle.dump(forest, open(model_file, 'wb'))

def predict():
    trained_model = pickle.load(open('traffic_model.pkl', 'rb'))

    abnormality_threshold = 4

    conn_log = "/opt/zeek/logs/current/conn.log"

    # Set up the inotify watcher
    watcher = inotify.adapters.Inotify()

    # Add the conn.log file to the watcher
    watcher.add_watch(conn_log)

    sc = StandardScaler()
    encoder = TargetEncoder(cols=['proto', 'service', 'state'], smoothing=1.0)

    # Continuously watch for changes to the conn.log file

    for event in watcher.event_gen():
        if event is not None:
            if "IN_MODIFY" in event[1]:
                with open(conn_log, "r") as f:
                    new_data = f.read()
                    entries = new_data.splitlines()

                    for entry in entries:
                        content = json.loads(entry)

                        ml_fields = [
                            content.get('duration', 0),
                            content.get('proto', ''),
                            content.get('service', ''),
                            content.get('conn_state',''),
                            content.get("orig_pkts", 0),
                            content.get("resp_pkts", 0),
                            content.get("orig_bytes", 0),
                            content.get("resp_bytes", 0),
                            content.get("orig_ip_bytes", 0) - content.get("orig_bytes", 0),
                            content.get("resp_ip_bytes", 0) - content.get("resp_bytes", 0),
                            content.get("orig_ip_bytes", 0) / content.get("orig_pkts", 0) if content.get("orig_pkts", 0) else 0,
                            content.get("resp_ip_bytes", 0) / content.get("resp_pkts", 0) if content.get("resp_pkts", 0) else 0,
                            content.get("orig_bytes", 0) / content.get("orig_pkts", 0) if content.get("orig_pkts", 0) else 0,
                            content.get("resp_bytes", 0) / content.get("resp_pkts", 0) if content.get("resp_pkts", 0) else 0
                        ]

                        ml_df = pd.DataFrame([ml_fields], columns=["dur", "proto", "service", "state", "spkts", "dpkts", "sbytes", "dbytes", "sloss", "dloss", "sinpkt", "dinpkt", "smean", "dmean"])
                        ml_df[['proto','service','state']] = encoder.transform(ml_df[['proto','service','state']])
                        ml_df = sc.transform(ml_df)
                        prediction = trained_model.predict(ml_df)
                        
                        if (prediction >= abnormality_threshold): {
                                # send data to DB to be stored and displayed on UI
                        }

def live_train():
    trained_model = pickle.load(open('traffic_model.pkl', 'rb'))

    conn_log = "/opt/zeek/logs/current/conn.log"

    # Set up the inotify watcher
    watcher = inotify.adapters.Inotify()

    # Add the conn.log file to the watcher
    watcher.add_watch(conn_log)

    sc = StandardScaler()
    encoder = TargetEncoder(cols=['proto', 'service', 'state'], smoothing=1.0)

    # Continuously watch for changes to the conn.log file

    for event in watcher.event_gen():
        if event is not None:
            if "IN_MODIFY" in event[1]:
                with open(conn_log, "r") as f:
                    new_data = f.read()
                    entries = new_data.splitlines()

                    for entry in entries:
                        content = json.loads(entry)

                        ml_fields = [
                            content.get('duration', 0),
                            content.get('proto', ''),
                            content.get('service', ''),
                            content.get('conn_state',''),
                            content.get("orig_pkts", 0),
                            content.get("resp_pkts", 0),
                            content.get("orig_bytes", 0),
                            content.get("resp_bytes", 0),
                            content.get("orig_ip_bytes", 0) - content.get("orig_bytes", 0),
                            content.get("resp_ip_bytes", 0) - content.get("resp_bytes", 0),
                            content.get("orig_ip_bytes", 0) / content.get("orig_pkts", 0) if content.get("orig_pkts", 0) else 0,
                            content.get("resp_ip_bytes", 0) / content.get("resp_pkts", 0) if content.get("resp_pkts", 0) else 0,
                            content.get("orig_bytes", 0) / content.get("orig_pkts", 0) if content.get("orig_pkts", 0) else 0,
                            content.get("resp_bytes", 0) / content.get("resp_pkts", 0) if content.get("resp_pkts", 0) else 0
                        ]

                        ml_df = pd.DataFrame([ml_fields], columns=["dur", "proto", "service", "state", "spkts", "dpkts", "sbytes", "dbytes", "sloss", "dloss", "sinpkt", "dinpkt", "smean", "dmean"])
                        ml_df[['proto','service','state']] = encoder.transform(ml_df[['proto','service','state']])
                        ml_df = sc.transform(ml_df)
                        prediction = trained_model.predict(ml_df)
                        trained_model.fit(ml_df, prediction)

if __name__ == '__main__':

    # These will be set depending on which button is pressed on UI
    live_training = 0
    predicting = 0
    training_file = 0
    
    # Live Train
    if (live_training == 1): {
        live_train() 
    }

    # Predict
    if (predicting == 1): {
        predict() 
    }

    # Train with existing file
    if (training_file == 1): {
        train_file() 
    }