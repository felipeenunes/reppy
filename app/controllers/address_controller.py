from flask.json import jsonify
from app.exc.exc import InvalidKeys, MissingKeys,InavlidValue
from app.models.address_model import AddressModel
from app.configs.database import db
from flask import current_app, jsonify

def create_address(address_data):
    keys = {'street','street_number','city','uf','zip_code'}

    missing_keys = list(keys.difference(set(address_data.keys())))

    if missing_keys:
        raise MissingKeys(','.join(missing_keys))

    invalid_keys = set(address_data.keys()).difference(keys)
    if invalid_keys:
        raise InvalidKeys(','.join(list(invalid_keys)))

    address_data['street'] = address_data["street"].title()
    address_data['uf'] = address_data["uf"].upper()

    states = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT','PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    if not address_data['uf'] in states:
        raise InavlidValue(','.join(list(address_data['uf'])))

    new_address = AddressModel(**address_data)

    db.session.add(new_address)
    db.session.commit()
    return new_address.id
    

def update_adress(address_data, address_id):
    if 'uf' in address_data: address_data['uf'] = address_data['uf'].upper()
    if 'street' in address_data: address_data['street'] = address_data['street'].title()

    updated_address = AddressModel.query.filter_by(id=address_id).update(address_data)
    current_app.db.session.commit()

    return 


def address_delete(address):
    address = AddressModel.query.get(address)
    db.session.delete(address)
    db.session.commit()
    return address
