
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

@cli.command('show')
@click.option('-t', '--table', help="Table's name")
@click.option('-f', '--format', 
	default='default',
	type=click.Choice(['default', 'hline', 'columns', 'cells', 'rows'], 
	case_sensitive=False)
)
def show(table, format):
	""" Add the SQLite path """
	query = Querys()
	query.show_table_names(format) if not table else query.show_table(table, format)