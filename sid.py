from steamid import get_64bit_steam_id
def gt32(id):
    data_file = get_64bit_steam_id(id)
    s32=int(data_file)-int(76561197960265728)
    return s32
def gt64(id):
    s64=get_64bit_steam_id(id)
    return s64