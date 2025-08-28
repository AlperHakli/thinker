from passlib.context import CryptContext

pwt_cxt = CryptContext()


def hash(plain_password) \
        -> str:
    """
    To hash a plain password

    :param plain_password: normal password
    :return: hashed password
    """
    return pwt_cxt.hash(plain_password)



def verify(plain_password, hashed_password) \
        -> bool:
    """
    :param plain_password: user password input
    :param hashed_password: hashed true password
    :return: if hashed plain password equals hashed_password True otherwise False
    """
    return pwt_cxt.verify(plain_password, hashed_password)

