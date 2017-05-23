#
# Script to import Abbott Freestyle data into Personal Data Logger Format Database, in this case CouchDB
# Usually has following columns
# ID,Time,Record Type,Historic Glucose (mg/dL),
# But user can add extra columns following the main columns to csv
# device,longitude,latitude,tags,note
# example1.csv = Basic Colums from FreeStyle  
# example2_added_columns.csv = Extra user added columns
#
#
# Author Thejesh GN
# License  GNU GPL v3
# How to use:
# python freestyle.py --inputfile example2.csv  --url https://api_key_user:api_key_password@username.cloudant.com --db personal_data --update 0

import click
import csv
import json
import couchdb
import md5
from datetime import datetime

@click.command()
@click.option('--inputfile', help='Input file is important. example2_added_columns.csv ')
@click.option('--url', prompt='url', help='url of DB. https://api_key_user:api_key_password@username.cloudant.com  ')
@click.option('--db', prompt='db', help='Couch DB. Like personal_data ')
@click.option('--update', prompt='update', default=0, help='Update existing records. 0 for No. 1 for Yes, update please. By default 0')

def hello(inputfile, url, db, update):
    couch = couchdb.Server(url)
    db = couch[db]

    first = True
    with open(inputfile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if first:
                first = False
                continue                
            doc = {}    
            #basic
            ID = row[0]
            time = row[1]
            m = md5.new()
            m.update(ID+time)
            #create an _id using md5 of ID and Time as per freestyle
            _id = m.hexdigest()
            exists = False
            try:
                if db[_id]:
                    print "Document with "+_id+" already exists."
                    doc = db[_id]
                    exists = True
            except couchdb.http.ResourceNotFound:
                #Create a new doc with _id
                exists = False
                doc["_id"] = str(_id)
                

            
            
            doc["version"] = 0.1
            #time format 2016/05/26 11:42
            #req "2016-05-26T11:42:00.00+05:30"
            datetime_object = datetime.strptime(time, '%Y/%m/%d %H:%M')
            #short cut, you need to use system timezone
            t = datetime_object.strftime("%Y-%m-%dT%H:%M")+"+05:30"
            doc["time"] = t                    
            doc["type"] = "cbg"
            data = {}
            
            ############################### additional fields ##################
            #These are additional fields that are added by user. 
            #But not a must
            if len(row) > 8:
                device = row[4]
                doc["device"] = device
                longitude = row[5]
                latitude = row[6]
                if longitude is None or longitude == "":
                    pass
                else:
                    geo  = { "type": "Point", "coordinates": [ longitude,latitude]},
                    doc["geo"] = geo
                
                tags = row[7]
                if tags is None or tags == "":
                    pass
                else:
                    doc["tags"] = [x.strip() for x in tags.split('|')]
                
                note = row[8]
                data["note"] = note
            ############################### additional fields ##################
            
            record = row[2]            
            glucose = row[3]
            data["glucose"] = int(glucose)
            data["unit"] ="mg/dL"
            doc['data'] = data
    
            print str(doc)
            if exists == False:
                db.save(doc)
                print "--------------------------- INSERTED -------------------"
            
            if exists == True and update == 1:                
                db.save(doc)
                print "---------------------------- UPDATED -------------------"
                
            
            
     
if __name__ == '__main__':
    hello()