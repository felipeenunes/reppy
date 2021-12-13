def filter_by_uf(republics, uf):
    if not uf: return republics
    
    return [i for i in republics if i.address.uf == uf.upper()]
