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
	""" Print all DB table names """
	cursor = connect_to_db()
	data = cursor.execute("SELECT name AS 'tables' FROM sqlite_master WHERE type='table';").fetchall()

	columns_name = [name[0] for name in cursor.description]	
	print_table(columns_name, data)



	




def connect_to_db():
	config = configparser.ConfigParser()
	config.read('.connection.conf')
	path = config['DB_CONNECTION'].get('path')	

	conn = sqlite3.connect(path)
	
	return conn.cursor()

def print_table(columns_name, data):
	# Converting the tuples to lists and the integers to strings, and adding spaces
	rows = [[str(value) for value in list(values)] for values in data]

	# zip() returns an iterator of tuples, taking elements in order from each iterable recieved as parameter
	# With * we break apart the list as parameters
	columns = list(zip(*rows))

	# creating tuples as [(first_el_l1, fisrt_el_l2), (second_el_l1, second)]
	sizes = [
		(len(max(max(data, key=len), column_name, key=len)) + 2)
		for (column_name, data) in zip(columns_name, columns)
	]

	# Creating the table
	line = ''
	columns_name_string = ''
	for size, name in zip(sizes, columns_name):
		line += ('+' + '-' * size )
		columns_name_string += ('| ' + name.ljust(size - 1, ' '))

	line += '+'
	columns_name_string += '|'

	click.echo(line)
	click.echo(columns_name_string)
	for row in rows:
		click.echo(line)
		row_string = ''
		for (size, value) in zip(sizes, row):
			row_string += '| ' + value.ljust(size - 1, ' ') 

		row_string += '|'
		click.echo(row_string)

	click.echo(line)