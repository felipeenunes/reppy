from app.models.address_model import AddressModel
from app.configs.database import db

def create_address(address_data):
    keys = ['street','street_number','city','uf','zip_code']
    for key in address_data:
        if not key in keys:
            raise KeyError
        if type(address_data[key]) != str: raise TypeError
    street = address_data["street"].title()
    street_number = str(address_data["street_number"])
    city = address_data["city"]
    uf = address_data["uf"].upper()
    zip_code = str(address_data["zip_code"])

    address = AddressModel(street=street, street_number=street_number, city=city, zip_code=zip_code, uf=uf)
    db.session.add(address)
    db.session.commit()
    return address.id
    

def update_adress(address_data, user):
    keys = ['street','street_number','city','uf','zip_code']
    for key in address_data:
        if not key in keys:
            raise KeyError
        if type(address_data[key]) != str: raise TypeError
    for i in address_data: 
        if type(i) != str: raise TypeError
    data = {}
    if 'uf' in address_data: data['uf'] = address_data['uf'].upper()
    if 'street' in address_data: data['street'] = address_data['street'].upper()
    if 'street_number' in address_data: data['street_number'] = str(address_data['street_number'])
    if 'city' in address_data: data['city'] = address_data['city']
    if 'zip_code' in address_data: data['zip_code'] = str(address_data['zip_code'])

    query = AddressModel.query.filter_by(id=user.address_id)
    for key, value in data.items():
        setattr(query,key,value)
    db.session.commit()
    data['uf'] = address_data['uf']
    return data


def address_delete(address):
    address = AddressModel.query.get(address)
    db.session.delete(address)
    db.session.commit()
    return address
