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



def import_csv(inputfile, update, db_manager):
    first = True
    with open(inputfile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if first:
                first = False
                continue                
            doc = None   
            #basic
            ID = row[0]
            time = row[1]
            m = md5.new()
            m.update(ID+time)
            #create an _id using md5 of ID and Time as per freestyle
            _id = m.hexdigest()
            exists = False
            doc = db_manager.getRecord(_id)
            if doc:
                print "Document with "+_id+" already exists."
                exists = True
                #NO need to update
                if update == 0:
                    continue
            else:
                #Create a new doc with _id
                doc = {}
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
                db_manager.addRecord(_id, doc)
                print "--------------------------- INSERTED -------------------"
            
            if exists == True and update == 1:                
                db_manager.updateRecord(_id, doc)
                print "---------------------------- UPDATED -------------------"
                
