import requests
from requests.exceptions import HTTPError
from flask import abort

class Mikrotik():
    #Initialize the mikrotik REST session
    def __init__(self, host: str, username: str, password: str, verify = True):
        self.https = 'https://' + host
        self.session = requests.Session()
        self.session.verify = verify
        self.session.auth = (username, password)
        self.session.headers.update({'Content-Type': 'application/json', 'Accepts': 'application/json'})
        
    def get(self, id = None):
        try:
            if id is None:
                r = self.session.get(self.https + '/rest/ip/dns/static')
            else:
                r = self.session.get(self.https + '/rest/ip/dns/static/' + id)
                  
            r.raise_for_status()
            return r.json()
            
        except HTTPError as exc:
            code = exc.response.status_code
            if code == 404:
              message = f"IPAM entry with id {id} not found"
            else:
              message = exc.response.json()['message']
            abort(
                code,
                message
            )
    
    def getByName(self, name):
        if name is None:
            abort(
                400,
                f"Name is required!"
            )
        
        ipamList = self.get()
        for ipam in ipamList:
            if ipam['name'] == name:
                return ipam
        
        return None
                
    def add(self, body):
        if 'name' in body:
            name = body['name']
            try:
                if self.getByName(name) == None:
                    r = self.session.put(self.https + '/rest/ip/dns/static', json=body)
                    r.raise_for_status()
                    return r.json()    
                else:
                    abort(
                        406,
                        f"IPAM entry  with fqdn {name} already exists"
                    )
            except HTTPError as exc:
                code = exc.response.status_code
                abort(
                    code,
                    exc.response.json()['message']
                )
        else:
            abort(
                400,
                f"Name is required!"
            )
            
    def update(self, id, body):
        ipam = self.get(id)
        try:
            if ipam != None:
                r = self.session.put(self.https + '/rest/ip/dns/static/' + id, json=body)
                r.raise_for_status()
                return r.json()
            else:
                abort(
                    404,
                    f"IPAM entry with ID {id} does not exist"
                )
        except HTTPError as exc:
            code = exc.response.status_code
            if code == 404:
              message = f"IPAM entry with id {id} not found"
            else:
              message = exc.response.json()['message']
            abort(
                code,
                message
            )
    
    def delete(self, id):
        try:
            r = self.session.delete(self.https + '/rest/ip/dns/static/' + id)
            r.raise_for_status()
            return '', r.status_code
        
        except HTTPError as exc:
            code = exc.response.status_code
            if code == 404:
              message = f"IPAM entry with id {id} not found"
            else:
              message = exc.response.json()['message']
            abort(
                code,
                message
            )