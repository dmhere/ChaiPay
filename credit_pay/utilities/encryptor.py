"""
@author: Deepak AGGARWAL
"""
import os

from cryptography.fernet import Fernet
from credit_pay.utilities import utils_config

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
utils_config_file_path = os.path.join(ROOT_DIR, 'utils_config.py')

config_encrypt_key = "encryption_key"


class Encryptor:
    key = utils_config.key['encryption_key']

    @staticmethod
    def encrypt(message):
        """
        encrypt input with the default key

        :param message: input to be encrypted
        :return: encrypted message
        """
        message = message.encode()
        return Fernet(Encryptor.key).encrypt(message).decode()

    @staticmethod
    def decrypt(token) -> bytes:
        """
        decrypt the token using the default key

        :param token: token to be decrypted
        :return: decrypted message
        """
        token = token.encode()
        return Fernet(Encryptor.key).decrypt(token).decode()


if __name__ == "__main__":
    print(Encryptor().encrypt("sk_test_51JG763SBWV6Cbihw1r7D3Xxplftx38c1xOGvYvJfBSAkROeQ8sZgNaGLRKr8wy16hOOnEPH58wbsD9A7kkrbjvgz007IGo2B0R"))
