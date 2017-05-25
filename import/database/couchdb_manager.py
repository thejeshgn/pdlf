import couchdb

class BaseDatabase(object):
    database = None
    db_type  = None
    db_url = None
    db_username = None
    db_password = None
    db_name = None

    def __init__(self, db_type, db_url, db_username, db_password, db_name):
        self.db_type     = db_type 
        self.db_url      = db_url
        self.db_username = db_username
        self.db_password = db_password
        self.db_name     = db_name

    def intialize():
        return None
    
    def checkIfTheRecordExists(_id):
        return None

    def addRecord(_id, document):
        return None
    
    def updateRecord(_id, document):
        return None
    
    def getRecord(_id):
        return None
    
    
class CouchDatabase(BaseDatabase):
    def intialize(self):
        full_url = "https://"+self.db_username+":"+self.db_password+"@"+self.db_url
        print str(couchdb)
        couch = couchdb.Server(full_url)
        self.database = couch[self.db_name]
                
    def checkIfTheRecordExists(self,_id):
        try:
            if self.database[_id]:
                print "checkIfTheRecordExists Document with "+_id+" already exists."
                return True
        except couchdb.http.ResourceNotFound:
            return False

    def addRecord(self,_id, document):
        return self.database.save(document)
        
    
    def updateRecord(self,_id, document):
        return self.database.save(document)
        

    def getRecord(self,_id):
        try:
            if self.database[_id]:
                print "getRecord Document with "+_id+" already exists."
                return self.database[_id]
        except couchdb.http.ResourceNotFound:
            return None  
            
            