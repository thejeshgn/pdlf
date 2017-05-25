from couchdb_manager import CouchDatabase

class DatabaseManager:

    def instance(self, db_type, db_url, db_username,db_password, db_name):    	
    	coouch_database = CouchDatabase(db_type, db_url, db_username, db_password, db_name)
        coouch_database.intialize()
        return coouch_database
