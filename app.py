
from models import DBConnection, Querys

import click

@click.group()
def cli():
	pass

@cli.command('connect')
@click.argument('path')
def connect_db(path):
	""" Add the SQLite PATH """
	DBConnection.write_config_file(path)

@cli.command('tables')
def show_tables():
	""" Print all DB table names """
	query = Querys()
	query.show_tables()

@cli.command('show')
@click.argument('table_name')
def show(table_name):
	""" Add the SQLite path """
	pass