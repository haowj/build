# coding:utf-8
__author__ = 'xcma'

# encoding:utf-8

from Crypto.Cipher import DES3
import base64

class prpcrypt():
    def __init__(self):
        self.mode = DES3.MODE_ECB
        self.BS = DES3.block_size
        self.key = 'superd-zjzy!@$%&*()asdfg'
    def pad(self,s):
        bw = self.BS - len(s) % self.BS
        if bw!=8:
            return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        else:
            return s

    def unpad(self,s):
        bw = self.BS - len(s) % self.BS
        if bw !=8:
            return s[0:-ord(s[-1])]
        return s

    def encrypt(self, text,is_base64=False):
        # 加密
        text = self.pad(text)

        cryptor = DES3.new(self.key, self.mode)
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)
        # print(text)
        self.ciphertext = cryptor.encrypt(text)
        if is_base64:
            data = base64.standard_b64encode(self.ciphertext).decode("utf-8")
        else:
            data = self.ciphertext
        return data


    def decrypt(self, text,is_base64=False):
        # 解密
        cryptor = DES3.new(self.key, self.mode)
        if is_base64:
            de_text = base64.standard_b64decode(text)
        else:
            de_text = text
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode("utf-8")).rstrip('\0')
        out = self.unpad(st)
        return out

des3 = prpcrypt()