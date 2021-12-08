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