import click
import sqlite3
import configparser

@click.group()
def cli():
	pass

@cli.command('connect')
@click.argument('connection')
def connect_db(connection):
	""" Add the SQLite path """
	config = configparser.ConfigParser()
	config['DB_CONNECTION'] = {"path" : connection}

	with open('.connection.conf', 'w') as configfile:
		config.write(configfile)

@cli.command('tables')
def show_tables():
	""" Printing all DB table names """
	cursor = connect_to_db()
	# data = cursor.execute("SELECT name AS 'tables' FROM sqlite_master WHERE type='table';").fetchall()
	data = cursor.execute("SELECT * FROM stocks").fetchall()
	# Getting a tuple with column names
	columns_name = [name[0] for name in cursor.description]	

	data_dict = organize_data(data, columns_name)

def connect_to_db():
	config = configparser.ConfigParser()
	config.read('.connection.conf')
	path = config['DB_CONNECTION'].get('path')	

	conn = sqlite3.connect(path)
	
	return conn.cursor()

def organize_data(data, columns_name):
	# Converting the tuples to lists and the integers to strings
	rows = [[str(value) for value in list(values)] for values in data]

	# zip() returns an iterator of tuples, taking elements from each iterable recieved as parameter,with * we 
	# break apart the list as parameters
	columns = list(zip(*rows))

	data_dict = {}

	for key, column_name in enumerate(columns_name):
		data = columns[key]
		# max return the largest item in an iterable or the largest of two or more arguments.
		# then we get the len of the word and we increment it in 2 for spaces
		longest_size = len(max(max(data, key=len), column_name, key=len)) + 2

		data_dict[column_name] = {
			'data': data,
			'size': longest_size
		}

	return data_dict