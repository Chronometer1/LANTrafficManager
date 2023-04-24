import random

from itertools import count

import tkinter as tk

from tkinter import *

from tkinter import ttk

from tkinter import filedialog

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pandas as pd

import numpy as np

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestRegressor

from category_encoders import TargetEncoder

import inotify.adapters

import json

import pickle

from tkinter import messagebox

import sqlite3

import time 



#Connect to DB

conn = sqlite3.connect('database.db')

c = conn.cursor()



#Check to see if table 1 already exists 

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='table1'")

result = c.fetchone()

if result:

	print("Table 'table1' already exists")

else:

	# Create table 1

	c.execute('''CREATE TABLE table1

				 (ID INT, max_depth INT, n_estimators INT, random_state INT, max_features INT,

				  min_samples_split INT, max_leaf_nodes INT, threshold REAL, flag_counter INT)''')

	c.execute("INSERT INTO table1 (ID, max_depth, n_estimators, random_state, max_features, min_samples_split, max_leaf_nodes, threshold, flag_count) \ VALUES (1, 4, 450, 3, 2, 75, 0, .5, 5)")

	conn.commit()

	print("Table 'table1' created")



#Checks to see if table 2 already exists

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='table2'")

result = c.fetchone()

if result:

	print("Table 'table2' already exists")

else:

	# Create table 2

	c.execute('''CREATE TABLE table2

				 (ID INT, ip_address INT UNSIGNED, packet_timestamp CHAR(30), ip_flag_count INT, duration INT,

				  rate INT, state INT, dload INT, dloss INT, classification INT)''')

	print("Table 'table2' created")



#commit and close changes

conn.commit()

conn.close()



# Connect to the database

conn = sqlite3.connect('database.db')

c = conn.cursor()



# Create increment_flag_count trigger





def check_flag_count():

	for row in c.execute('SELECT * FROM table2'):

		ip_address = table2.item(row, "values")[0]

		ip_flag_count = int(table2.item(row, "values")[2])

		if ip_flag_count > 5:

			messagebox.showinfo("Flag Counter Alert", f"IP address with flag counter above threshold: {ip_address}")

			break



global prediction



# Set up UI window

root = tk.Tk()

root.geometry("1200x800")

root.title("Traffic Monitor")



# Set up notebook

notebook = ttk.Notebook(root)

notebook.pack(fill='both', expand=True)



# Define flag variable

capture_data = False



# Define button functions

def start_capture():

	global capture_data

	capture_data = True

	predict()	



def stop_capture():

	global capture_data

	capture_data = False



def browseFiles():

	filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files", "*.*")))

	train_file(filename)  



# Home Tab

Home = ttk.Frame(notebook)

notebook.add(Home, text='Home')



button_ex = ttk.Button(Home, text="Exit",command= exit)

button_ex.pack(anchor=E)



button_tfc = ttk.Button(Home, text="Train from capture")

button_tfc.pack(anchor=W)



button_sc = ttk.Button(Home, text="Start capture", command=start_capture)

button_sc.pack(anchor=W)



button_ec = ttk.Button(Home, text="Stop capture", command=stop_capture)

button_ec.pack(anchor=W)



button_tff = ttk.Button(Home, text="Train from file", command=browseFiles)

button_tff.pack(anchor=W)



# Define blue label for the graph

label_buffer = ttk.Label(Home, background="blue")

label_buffer.pack(expand=True, fill=tk.BOTH)



# settings Tab



# Define function to insert settings into the "table1" table

def insert_settings(max_depth, n_estimators, random_state, max_features, min_samples_split, max_leaf_nodes, threshold, flag_counter):

	c.execute("""

		INSERT INTO table1 (max_depth, n_estimators, random_state, max_features, min_samples_split, max_leaf_nodes, threshold, flag_counter)

		VALUES (?, ?, ?, ?, ?, ?, ?, ?)

	""", (max_depth, n_estimators, random_state, max_features, min_samples_split, max_leaf_nodes, threshold, flag_counter))

	conn.commit()

	print("Settings inserted into table1")



# Define function to handle user input

def apply_settings():

	# Get user input values

	max_depth_val = int(max_depth.get())

	n_estimators_val = int(Num_Est.get())

	random_state_val = int(Random_St.get())

	max_features_val = int(Max_Fea.get())

	min_samples_split_val = int(Min_Sam.get())

	max_leaf_nodes_val = int(Max_Lea.get())

	threshold_val = float(Abn_Thr.get())

	flag_counter = int(Flag_Count.get())



	# Insert user input values into "table1"

	insert_settings(max_depth_val, n_estimators_val, random_state_val, max_features_val, min_samples_split_val, max_leaf_nodes_val, threshold_val, flag_counter)



# Create a new "ttk.Frame" for the settings tab

Settings = ttk.Frame(notebook)

notebook.add(Settings,text="Settings")



# Create "tk.StringVar" objects to hold the values of the Entry widgets

maxDep = tk.StringVar()

numEst = tk.StringVar()

ranSta = tk.StringVar()

MaxFea = tk.StringVar()

MinSam = tk.StringVar()

MaxLea = tk.StringVar()

AbnThr = tk.StringVar()

FlagCount = tk.StringVar()



# Create "tk.Entry" widgets for the user to input values

max_depth_label = ttk.Label(Settings, text="Max Depth")

max_depth_label.pack(anchor=W)

max_depth = tk.Entry(Settings)

max_depth.pack(fill='both', pady=10)



num_est_label = ttk.Label(Settings, text="Number of Estimates")

num_est_label.pack(anchor=W)

Num_Est = tk.Entry(Settings)

Num_Est.pack(fill='both', pady=10)



random_state_label = ttk.Label(Settings, text="Random State")

random_state_label.pack(anchor=W)

Random_St = tk.Entry(Settings)

Random_St.pack(fill='both', pady=10)



max_features_label = ttk.Label(Settings, text="Max Features")

max_features_label.pack(anchor=W)

Max_Fea = tk.Entry(Settings)

Max_Fea.pack(fill='both', pady=10)



min_samples_label = ttk.Label(Settings, text="Minimum Samples")

min_samples_label.pack(anchor=W)

Min_Sam = tk.Entry(Settings)

Min_Sam.pack(fill='both', pady=10)



max_layers_label = ttk.Label(Settings, text="Max Layers")

max_layers_label.pack(anchor=W)

Max_Lea = tk.Entry(Settings)

Max_Lea.pack(fill='both', pady=10)



abnormality_threshold_label = ttk.Label(Settings, text="Abnormality Threshold")

abnormality_threshold_label.pack(anchor=W)

Abn_Thr = tk.Entry(Settings)

Abn_Thr.pack(fill='both', pady=10)



Flag_Count_label = ttk.Label(Settings, text="Flag Count")

Flag_Count_label.pack(anchor=W)

Flag_Count = tk.Entry(Settings)

Flag_Count.pack(fill='both', pady=10)



# Create a "tk.Button" widget to apply the user input values

Apply = tk.Button(Settings, text="Apply", command=apply_settings)

Apply.pack()



# Set up graph

plt.style.use('fivethirtyeight')

fig, ax = plt.subplots()

x_vals = []

y_vals = []

line, = ax.plot(x_vals, y_vals)





# Define animation function

def animate(i,prediction): 



	if capture_data:

		x_vals.append(next(index))

		y_vals.append(prediction)

		if len(x_vals) > 250:

                       x_vals.pop(0)

                       y_vals.pop(0)

		line.set_data(x_vals, y_vals)

		ax.relim()

		ax.autoscale_view()

		plt.pause(0.01)

		canvas.draw()

		check_flag_count()

index = count()



# Create canvas and add to UI window

canvas = FigureCanvasTkAgg(fig, master=label_buffer)



# canvas.draw()

canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)



def train_file(filename):

	# Variables to store values pulled from settings screen in UI

	train_file = filename

	n_estimators_val = 450

	max_features_val = 2

	random_state_val = 3

	max_depth_val = 4

	min_samples_leaf_val = 75



	train = pd.read_csv(train_file)



	encoder = TargetEncoder(cols=['proto', 'service', 'state'], smoothing=1.0)

	train[['proto', 'service', 'state']] = encoder.fit_transform(train[['proto', 'service', 'state']], train['label'])



	encoder_file = 'encoder.pkl'

	pickle.dump(encoder, open(encoder_file,'wb'))



	X_train = train.iloc[:, 1:15].values

	y_train = train.iloc[:, 15].values



	sc = StandardScaler()

	X_train = sc.fit_transform(X_train)

	scanner_file = 'scanner.pkl'

	pickle.dump(sc, open(scanner_file, 'wb'))

	forest = RandomForestRegressor(n_estimators = n_estimators_val, max_features = max_features_val, random_state = random_state_val, max_depth = max_depth_val, min_samples_leaf = min_samples_leaf_val)

	forest.fit(X_train, y_train)



	model_file = 'traffic_model.pkl'

	pickle.dump(forest, open(model_file, 'wb'))



def predict():

	trained_model = pickle.load(open('traffic_model.pkl', 'rb'))

	encoder = pickle.load(open('encoder.pkl','rb'))

	sc = pickle.load(open('scanner.pkl','rb'))

	abnormality_threshold = 4

	conn_log = "/opt/zeek/logs/current/conn.log"



	# Set up the inotify watcher

	watcher = inotify.adapters.Inotify()



	# Add the conn.log file to the watcher

	watcher.add_watch(conn_log)



	# Continuously watch for changes to the conn.log file

	if capture_data:

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

							animate(None,prediction)

							print(prediction)



							# animate(prediction)

							if prediction >= abnormality_threshold:

								ip_address = content.get('id.orig_h')

								# Check if the IP address already exists in the table

								c.execute("SELECT ip_flag_count FROM table2 WHERE ip_address = ?", (ip_address,))

								row = c.fetchone()

								if row:

									# If the IP address exists, increment the flag_count value

									updated_flag_count = row[0] + 1

									c.execute("UPDATE table2 SET ip_flag_count = ? WHERE ip_address = ?", (updated_flag_count, ip_address))

								else:

									# If the IP address doesn't exist, insert a new record with flag_count set to 1

									c.execute("INSERT INTO table2 (ip_address, classification, ip_flag_count) VALUES (?, ?, ?)", (ip_address, prediction, 1))     

								conn.commit()



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



# Start UI loop

root.mainloop()
