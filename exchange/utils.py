import string
import random

def invite_code(chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(6))
