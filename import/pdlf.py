import sys, os
sys.path.append(os.path.dirname(__file__))

import click
import config
from database import manager
from abbott import freestylelibre

@click.command()
@click.option('--method', help='method. method')
@click.option('--inputfile', help='Input file is important. example2_added_columns.csv ')
@click.option('--update', prompt='update', default=0, help='Update existing records. 0 for No. 1 for Yes, update please. By default 0')
def abott_freestylelibre(method, inputfile, update):    
    print "START importing abott_freestylelibre"
    db_manager = manager.DatabaseManager()
    custom_manager = db_manager.instance(config.DB_TYPE, config.DB_URL, config.DB_USERNAME, config.DB_PASSWORD, config.DB_NAME)
    freestylelibre.import_csv(inputfile, update, custom_manager)
    print "END importing abott_freestylelibre"

if __name__ == '__main__':
    abott_freestylelibre()    