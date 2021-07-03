import hashlib as hs

def md5(text):
        salt ="22"
        bytes = (text+salt).encode() 
        readable_hash = hs.md5(bytes).hexdigest();
        return readable_hash