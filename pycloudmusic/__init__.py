# limit
LIMIT = 8
DOWNLOAD_PATH = "./download"
# chunk size
CHUNK_SIZE = 1024
RECONNECTION = 3

def _id_format(id_, dict_str=False):
    if type(id_) == str or type(id_) == int:
        format_str = str([{"id": id_}]) if dict_str else str([id_])
    elif type(id_) == list and dict_str:
        list_ = []
        for data in id_:
            list_.append({"id": data})
        format_str = str(list_)
    else:
        format_str = str(id_)

    return format_str

from pycloudmusic.music163 import LoginMusic163, Music163Api