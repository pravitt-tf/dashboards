import random
import string

def generate_key(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

if __name__ == "__main__":
    key = generate_key()
    print("Generated Key:", key)