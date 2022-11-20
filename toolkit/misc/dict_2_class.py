class Dict2Class:
    def __init__(self, my_dict):
        for key in my_dict:
            mapped_key = key.lower().replace(" ", "_")
            setattr(self, mapped_key, my_dict[key])