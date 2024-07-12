from init import init
from logger import log_msg
from enums import HashModes


def hashcat_entrypoint():
    args = init()
    hash_function = HashModes.get_hash_function_map()[args.mode]
    hash_obj = hash_function()
    hash_obj.update("abc".encode("utf-8"))
    hash = hash_obj.hexdigest()
    log_msg(hash)


if __name__ == '__main__':
    hashcat_entrypoint()