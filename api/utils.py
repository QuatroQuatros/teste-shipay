import bcrypt
import random
import string


def generate_random_password(length=8):
    #gera uma senha aleatoria
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_password_hash(password):
    # Gera uma hash para a senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def check_password(text, hashed_password):
    # Verifica se o texto corresponde à hash
    return bcrypt.checkpw(text.encode('utf-8'), hashed_password.encode('utf-8'))