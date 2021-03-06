from app.exc.exc import BadRequestError


def filter_by_uf(republics, uf):
    if not uf: return republics
    
    return [i for i in republics if i.address.uf == uf.upper()]


def verification(data,keys):
    missing_keys=[]
    value_incorrect = []
    for key,value in keys.items():
            if not key in data:
                missing_keys.append(key)
            if (key in data) and (value != type(data[key])):
                value = str(value).replace("<class ", "").replace(">", "")
                inserted_type = type(data[key])
                inserted_type = str(inserted_type).replace("<class ", "").replace(">", "")
                raise BadRequestError({ "Invalid type for": key,
                                        "Inserted type": inserted_type[1:-1], 
                                        "correct type": value[1:-1]
                                        })
    if missing_keys: raise BadRequestError(f'Required keys not found: {missing_keys}')
    if value_incorrect: raise BadRequestError(f'Invalid data type: {value_incorrect}')

