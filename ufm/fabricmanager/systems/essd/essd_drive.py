import sys
import redfish
import json
import time
from redfish.rest.v1 import redfish_client


class EssdDrive():
    def __init__(self, url, username=None, password=None, logger=None):
        self.url=url
        self.username=username
        self.password=password
        self.logger=logger
        self.essdPrefix="/essd/"

        self.root = redfish_client(base_url=(self.url), timeout=1, max_retry=1)
        self.uuid = self.root.root['UUID']


    def __del__(self):
        if hasattr(self, 'root'):
            self.root.logout()


    def get(self, request):
        response = self.root.get(request, headers=None)
        if response.status != 200:
           return response.status, request, {}

        value = json.dumps(response.dict, indent=4, sort_keys=True)
        return response.status, request, json.loads(value)


    def printAllMembers(self, key, jsonData):
        '''
          Prints main members in a jsom message
        '''
        print("-"*60)
        print("key={}".format(key))
        for x in jsonData:
            print("  {}: {}".format(x, jsonData[x]))
        print("-"*60)


    def removeDuplicates(self, string):
        result=[]
        lastChar=''
        for char in string:
            if char == '/' and char == lastChar:
                lastChar=char
                continue

            result.append(char)
            lastChar=char

        return ''.join(result)


    def addPrefix(self, tag, uuid, key):
        return self.removeDuplicates(tag + "/" + str(uuid) + "/" + str(key))


    def save(self, db, key, jsonData):
        if db == None:
            return

        # If uuid doesn't exist, no data can be saved to DB
        if self.uuid == None:
            return

        keyWithPrefix = self.addPrefix(self.essdPrefix, self.uuid, key)

        try:
            value = db.get_key_value(keyWithPrefix).decode('utf-8')
            if value == jsonData:
                return
        except:
            pass

        db.save_key_value(keyWithPrefix, jsonData)


    def updateUuid(self, db):
        if db == None:
            return

        tmpString=''
        lastUpdateKey = "/essd/uptimes"
        try:
            tmpString = db.get_key_value(lastUpdateKey).decode('utf-8')
        except:
            pass

        uuids = dict()
        if tmpString:
            uuids = json.loads(tmpString)

        new_uuids = dict()
        for u in uuids:
            new_uuids[u] = uuids[u]

        # Update current uptime
        new_uuids[self.uuid] = int(time.time())
        jsonString = json.dumps(new_uuids, indent=4, sort_keys=True)

        db.save_key_value(lastUpdateKey, jsonString)


    def removeUuidOlderThan(self, db, sec):
        if db == None:
            return

        tmpString=''
        lastUpdateKey = "/essd/uptimes"
        try:
            tmpString = db.get_key_value(lastUpdateKey).decode('utf-8')
        except:
            return

        uuids = dict()
        if tmpString:
            uuids = json.loads(tmpString)

        allUptimes = uuid.values()
        latestUptime = max(allUptimes)

        remove_uuids = dict()
        keep_uuids = dict()
        for u in uuids:
            uptime=uuids[u]
            if uptime + sec < latestUptime:
                remove_uuids[u] = uuids[u]
            else:
                keep_uuids[u] = uuids[u]

        # Update the update list
        jsonString = json.dumps(keep_uuids, indent=4, sort_keys=True)
        db.save_key_value(lastUpdateKey, jsonString)

        if not bool(remove_uuids):
            return

        for u in remove_uuids:
            db.delete_key_value("/essd/" + u)


    def readEssdSystemsData(self, db):
        status, key, jsonSystems = self.get(request="/redfish/v1/Systems")
        if status != 200:
            return

        self.save(db, key, jsonSystems)
        count = jsonSystems['Members@odata.count']
        for i in range(count):
            member = jsonSystems['Members'][i]['@odata.id']
            status, key, jsonMembers = self.get(request=member)
            if status != 200:
                continue

            self.save(db, key, jsonMembers)
            storage = jsonMembers['Storage']['@odata.id']
            status, key, jsonStorage = self.get(request=storage)
            if status != 200:
                continue

            self.save(db, key, jsonStorage)
            memberDrive = jsonStorage['Members']
            for drive in memberDrive:
                x = drive['@odata.id']
                status, key, jsonStorageMember = self.get(request=x)
                if status != 200:
                    continue

                self.save(db, key, jsonStorageMember)
                drives = jsonStorageMember['Drives']
                for d in drives:
                    driveId = d['@odata.id']
                    status, key, jsonDrives = self.get(request=driveId)
                    if status != 200:
                        continue

                    self.save(db, key, jsonDrives)


    def readEssdData(self, db):
        # Reads data from essd drive and writes it to db
        key="/redfish/v1"
        jsonData = self.root.root

        self.save(db, key, jsonData)
        for root in jsonData:
            if root == "Systems":
                self.readEssdSystemsData(db)

            if root == "Chassis":
                # TODO
                pass

            if root == "Managers":
                # TODO
                pass

            if root == "JsonSchemas":
                # TODO
                pass



