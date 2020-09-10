import configparser
import sqlite3
import click

class DBConnection:
	""" Define all the methods to manage the connection """
	def __init__(self):
		self.connect_to_db()

	@staticmethod
	def write_config_file(path):
		config = configparser.ConfigParser()
		config['DB_CONNECTION'] = {'path' : path}
		with open('.connection.conf', 'w') as configfile:
			config.write(configfile)

	def __read_config_file(self):
		config = configparser.ConfigParser()
		config.read('.connection.conf')
		return config['DB_CONNECTION'].get('path')	

	def connect_to_db(self):
		db_file = self.__read_config_file()
		conn = sqlite3.connect(db_file)
		# Create the cursor for querys to sqlite
		self.cursor = conn.cursor()



class Querys:
	""" Define all the querys """
	def __init__(self):
		self.new_connection = DBConnection()

	def __get_columns_name(self):
		return [name[0] for name in self.new_connection.cursor.description]

	def show_tables(self):
		data = self.new_connection.cursor.execute(
			"SELECT name AS 'tables' FROM sqlite_master WHERE type='table';"
		).fetchall()

		columns_name = self.__get_columns_name()

		printable = PrintTable(columns_name, data)
		printable.print()


class PrintTable:
	""" Printing style methods """
	def __init__(self, columns_name, data):
		self.columns_name = columns_name
		self.data = data
		self.__organize_data()

	def __organize_data(self):
		# Converting the tuples to lists and the integers to strings, and adding spaces
		self.rows = [[str(value) for value in list(values)] for values in self.data]

		# zip() returns an iterator of tuples, taking elements in order from each iterable recieved as parameter
		# With * we break apart the list as parameters
		columns = list(zip(*self.rows))

		# creating tuples as [(first_el_l1, fisrt_el_l2), (second_el_l1, second)]
		self.sizes = [
			(len(max(max(values, key=len), column_name, key=len)) + 2)
			for (column_name, values) in zip(self.columns_name, columns)
		]

	def print(self):
		# Creating the table
		line = ''
		columns_name_string = ''
		for size, name in zip(self.sizes, self.columns_name):
			line += ('+' + '-' * size )
			columns_name_string += ('| ' + name.ljust(size - 1, ' '))

		line += '+'
		columns_name_string += '|'

		click.echo(line)
		click.echo(columns_name_string)
		click.echo(line)
		for row in self.rows:
			row_string = ''
			for (size, value) in zip(self.sizes, row):
				row_string += '| ' + value.ljust(size - 1, ' ') 

			row_string += '|'
			click.echo(row_string)

		click.echo(line)