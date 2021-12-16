from app.exc.exc import BadRequestError
from app.models.address_model import AddressModel
from app.configs.database import db
from flask import current_app
from . import verification


def create_address(address_data):
    keys = {'street':str,'street_number':str,'city':str,'uf':str,'zip_code':str}

    new_data={}
    verification(address_data,keys)
       
    for key in address_data:
        if key in keys:
            new_data[key] = address_data[key]   

    new_data['street'] = address_data["street"].title()
    new_data['uf'] = address_data["uf"].upper()

    states = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT','PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    if not new_data['uf'] in states:
        raise BadRequestError(f'Invalid UF value: {",".join(list(new_data["uf"]))}')

    new_address = AddressModel(**new_data)

    db.session.add(new_address)
    db.session.commit()
    return new_address.id
    

def update_adress(address_data, address_id):
    keys = {'street':str,'street_number':str,'city':str,'uf':str,'zip_code':str}
    types_keys = {key:value for key,value in keys.items() if key in address_data}
    verification(address_data,types_keys)
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
