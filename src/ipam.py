import os
from mikrotik import Mikrotik
mikrotik = Mikrotik(os.getenv('API_HOST'), os.getenv('API_USERNAME'), os.getenv('API_PASSWORD'), os.getenv('API_VERIFY'))

def get_all():
    return mikrotik.get()

def get_one(id):
    return mikrotik.get(id)

def add_new(ipam):
    return mikrotik.add(ipam)

def update_one(id, ipam):
    return mikrotik.update(id, ipam)

def delete_one(id):
    return mikrotik.delete(id)