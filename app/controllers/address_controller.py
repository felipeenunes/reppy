from flask import request
from app.exc.exc import InvalidZipCode
from app.models.address_model import AddressModel
from app.models.state_model import StateModel
from app.configs.database import db

def create_address(address_data):
    street = address_data["street"].title()
    street_number = address_data["street_number"]
    city = address_data["city"]
    uf = address_data["uf"].upper()
    uf_id = StateModel.query.filter_by(uf=uf).first().id
    zip_code = address_data["zip_code"]

    address = AddressModel(street=street, street_number=street_number, city=city, uf_id=uf_id, zip_code=zip_code)
    db.session.add(address)
    db.session.commit()
    return address.id
    

def update_adress(address_data, user):
    for i in address_data: 
        if type(i) != str: raise TypeError
    data = {}
    if 'uf' in address_data: data['uf'] = address_data['uf'].upper()
    if 'street' in address_data: data['street'] = address_data['street'].upper()
    if 'street_number' in address_data: data['street_number'] = address_data['street_number']
    if 'city' in address_data: data['city'] = address_data['city']
    if 'zip_code' in address_data: data['zip_code'] = address_data['zip_code']
    if 'uf' in address_data:
        data['uf_id'] = AddressModel.uf_id = StateModel.query.filter_by(uf=data['uf']).first().id
        del data['uf']

    query = AddressModel.query.filter_by(id=user.address_id)
    for key, value in data.items():
        setattr(query,key,value)
    db.session.commit()
    del data['uf_id']
    data['uf'] = address_data['uf']
    return data


def address_delete(address):
    address = AddressModel.query.get(address)
    db.session.delete(address)
    db.session.commit()
    return address
