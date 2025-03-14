import json

import bcrypt
from Crypto.Util.Padding import unpad

DEFAULT_ENCODE = 'utf-8'

class BcryptVersion:

    PREFIX_2A = "2a"

    PREFIX_2Y ="2y"

    PREFIX_2B ="2b"

    def __init__(self, value: str = None):
        if not value:
            value = BcryptVersion.PREFIX_2A
        self.version = value

    def get_version(self):
        return self.version


def bcrypt_version_2a() -> BcryptVersion:
    return BcryptVersion(BcryptVersion.PREFIX_2A)


def bcrypt_version_2b() -> BcryptVersion:
    return BcryptVersion(BcryptVersion.PREFIX_2B)


def bcrypt_version_2y() -> BcryptVersion:
    return BcryptVersion(BcryptVersion.PREFIX_2Y)


def bcrypt_hash_password(password: str, version: BcryptVersion = None, rounds: int = 10, encode: str = DEFAULT_ENCODE):
    """
    将密码哈希并存储哈希值
    :param password: 明文密码
    :param version: bcrypt加密版本
    :param rounds: 生成盐，指定成本因子
    :param encode: 编码 utf-8
    :return: 加密值
    """
    if not version:
        version = bcrypt_version_2a()
    password_bytes = password.encode(encode)  # 将密码转换为字节
    prefix = version.get_version().encode(encode)
    salt = bcrypt.gensalt(prefix=prefix, rounds= rounds)  # 生成盐
    hashed_password = bcrypt.hashpw(password_bytes, salt)  # 生成哈希
    return hashed_password


def bcrypt_check_password(stored_hash, password_to_check, encode: str = DEFAULT_ENCODE):
    #用户登录时，验证提交的密码是否正确

    # 将密码转换为字节
    if isinstance(password_to_check, str):
        password_bytes = password_to_check.encode(encoding=encode)
    elif isinstance(password_to_check, bytes):
        password_bytes = password_to_check
    else:
        password_bytes = str(password_to_check).encode(encoding=encode)

    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode(DEFAULT_ENCODE)

    return bcrypt.checkpw(password_bytes, stored_hash)  # 检查密码



from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def aes_encrypt_data(data, key, iv: str = None, decode: str = DEFAULT_ENCODE):
    # 数据必须是16字节的倍数，所以需要填充
    def pad(data):
        return data + (16 - len(data) % 16) * chr(16 - len(data) % 16).encode()

    # 初始化数据
    if isinstance(data, bytes):
        data = data.decode(decode)

    data = pad(data.encode(decode))
    if isinstance(key, str):
        key = key.encode(decode)

    if not iv:
        if not isinstance(key, bytes):
            iv = key[0:AES.block_size]
        else:
            iv = key.decode(decode)[0:AES.block_size]

    iv = iv.encode(decode)

    # 创建加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 加密数据
    encrypted_data = cipher.encrypt(data)
    # 返回Base64编码的数据，以便安全传输
    return base64.b64encode(encrypted_data).decode()


def aes_decrypt_data(encrypted, key, iv= None, encode: str = DEFAULT_ENCODE):
    encrypted = base64.b64decode(encrypted)
    if not iv:
        if isinstance(key, bytes):
            iv = key.decode(encode)[0: AES.block_size]
        else:
            iv = key[0: AES.block_size]

    if not isinstance(key, bytes):
        key = key.encode(encode)
    if not isinstance(iv, bytes):
        iv = iv.encode(encode)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode(encode, 'ignore')


def __test_bcrypt():
    original_password = 'admin123'
    hashed_password = bcrypt_hash_password(original_password)  # 哈希密码
    # java encrypt
    pd = b'$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2'
    print("Hashed password:", hashed_password)

    # 假设用户稍后尝试登录，我们需要验证他们的密码
    password_attempt = 'admin123'
    if bcrypt_check_password(hashed_password, password_attempt):
        print("Password is correct!")
    else:
        print("Password is incorrect.")

    if bcrypt_check_password(pd, password_attempt):
        print("pd1 Password is correct!")
    else:
        print("pd1 Password is incorrect.")


def __test_aescrypt():
    # 密钥必须是16、24或32字节长
    key = get_random_bytes(16)

    key = "694390bf-c759-4f5a-8444-723b46d4".encode("utf-8")

    # key = b'694390bf-c759-4f'

    # 待加密的数据
    data = '{"username":"admin","password":"admin123","code":"11"}'

    # 加密
    encrypted = aes_encrypt_data(data, key)
    print('Encrypted:', encrypted)

    # 解密
    decrypted = aes_decrypt_data(encrypted, key)
    print('Decrypted:', decrypted)

    json_data = '{"params":"fJ9iM6kneIOpeX+nwpeXY/JoLsb8SwH3J9Ptx9Ou7UkE32diLBxRJ/hAOTJPz9qpvA+RMwPw73EintpDL+G1ZQ==","encrypt":true}'
    jd = json.loads(json_data)
    params = jd.get("params")

    ret = aes_decrypt_data(params, key)
    print(ret)

if __name__ == '__main__':
    # 示例用法
    # __test_bcrypt()

    __test_aescrypt()
