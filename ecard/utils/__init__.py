import execjs
from . import jscontent

context = execjs.compile(jscontent.JS)


def encryptString(exponent, modulus, str):
    """Rsa加密"""
    return context.call('encryptString', exponent, modulus, str)
