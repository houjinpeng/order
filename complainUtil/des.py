from Cryptodome.Cipher import AES
import os
from Cryptodome import Random
import base64



class AESUtil:

    __BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size

    @staticmethod
    def encryt(str, key, iv):
        cipher = AES.new(key, AES.MODE_CBC,iv)
        x = AESUtil.__BLOCK_SIZE_16 - (len(str) % AESUtil.__BLOCK_SIZE_16)
        if x != 0:
            str = str + chr(x)*x
        msg = cipher.encrypt(str)
        # msg = base64.urlsafe_b64encode(msg).replace('=', '')
        msg = base64.b64encode(msg)
        return msg

    @staticmethod
    def decrypt(enStr, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # enStr += (len(enStr) % 4)*"="
        # decryptByts = base64.urlsafe_b64decode(enStr)
        decryptByts = base64.b64decode(enStr)
        msg = cipher.decrypt(decryptByts)
        paddingLen = ord(msg[len(msg)-1])
        return msg[0:-paddingLen]


if __name__ == '__main__':
    key = "0123456789abcdef".encode('utf-8')
    iv = b"0123456789abcdef"
    # a = "qY0PirHsr0zFBHdg6IlMgmWgGuvuJxPB5dgHRlJ2Vl4mcdyocqXKC9I9sz9hZf7OXjtOCpFFS1V6WumvnaxE4cybZbypsIgUUN+mAnuRhavzsvlQ1Gs3K7ajEhnwP6cGrfAyDx1rDsNIylSOcXsrP8mze2ZwWDqgpl0w1YamJnlHIVR5YHBmhdV5pMnGGUpmPtprgyqWQpwklXH/HTxrWSyXJvzBAx4Mu31ocbjJnxVU69dlAOMg0NQW51GdsFpG4mGSkQpBpl2y68NmxftVFLOk64fdkFoRLetcef7pim8oVhMZkE5ivsOPgtc9gYV0rS0GMIJn3HmdktjHeK7VFd1XnLUyNsi6/v/TE1o0eltEltehIlpkniFNB2glvk696hzTvrWQLGosGW0GxpAmQ6RcLfv4upwsZfTgn9oPjqeKz33q61KcqwS7nySl+FwbAo16akKFIGs6M8vzP0Ipx69ijT4aoT8i2JM5GKCLXG7SS7YSR7QE1mbnMbuppp9ywbKiJi/4dor5oEEMNCT6/gzgcDS4D3Li2+ApWNMLTuvEbRdtVx0UI0ytsJGgv0eag0PBDcks1vbTAZi59+LQlqCVrypIneRYJDsFaiRAsMY3Z/MRy8LuDqueaEP/LrkIHBP9inuOp6kxnlN5kKGEbH1AxB2F1+lSgdcPBTMYmk3xfm4Olw8hDH1AxB2F1+lSNBNxvPVA0RMsGcV9tjDR/Q9r/Wi9i8GpJxSIoGK9X1eWQ4R4HrWwT1CfAW6xwbWnAJ3gs/afM+TL3hIxOijRO58xD365fpExpRqNn2WwAH7ZXcbuhfWB9iN9LgG4NtbvRYMi/xi2yDjgairQKkZ5Bae5Z24/he4zq8F53CsOTOwQ0qNfSAjKBGn6GFqimoM8+pk31+m0e4ZhgLNYhW2xbICsVjlzCRUVeRIeDNsRXubf+saQuxElz31AxB2F1+lSZkzkDjSFFXe/srlQrd/zIuC2QDKv6TQQnp3Rv6I/X1ujFT81Om4WWE6B+Wnr6hYo+LypRQOXpbzWuF3u3s0HQdvH3VRbkFpPUjIMMGzzBF2p42UvaboPdbVa4SvOrBnh8uujOUf7ErJps3MNb8Ag3b4+liU5EU0Hvj6WJTkRTQdLXN3hghNipzzQhpDbJqSPniuLNAHSxBrDAxftORNINcMDF+05E0g16+2M57E9TEpu0Uk+5mg3xq75k1vQgXkkuXyvRfIbzHe5fK9F8hvMd50eHkNRgz71+pwa67bC15Hsfckop5+ZkWlzRb0Pd5T0qFuboh1Xws6H36/EWkO59rGE4kvzlR7u1PvfsM6BIPN0Pdzwr+mtOzumB8bVdKWUu323uoss1x6mDS/jexhuC1aruIVmdMKn/DTn6Bd4XOVwxa3KOc+08sPRu5URVqYZQNcKPJwFgTTOfbflgJLNCFlpVECJMB3R+wAZ6RPZIpHC95+z0lwpH1pcixr8nULots5pPf6EBCn/PrVa3wwudb4+liU5EU0HSHnJNJrVbdnNGBtgLSNr5a/ktEEyTDU+niuLNAHSxBoRNS0B80NtPsMDF+05E0g1wwMX7TkTSDX50ft4KBUnkvlBHSqBTzYJbtFJPuZoN8bt3PrBbKnl1WClLqQqSG5U4FBYdfPdXyFHIf8uaw/TADWCPqVijJtTgdD/G9EOPHKrRwHKwkW08h0sTjWn9UC6SBx2MDGXtmpIHHYwMZe2amahTsAp1tTZS1zd4YITYqc80IaQ2yakjxfN1jiiLZEL8ZuJZtB+LvDhzhZg+5Mo8YHQ/xvRDjxyq0cBysJFtPIdLE41p/VAuq57xRH+ODXgPHiPjmbOXTr2yBAkNDAk9Qhq+UUSKpil7WC4KbJ47K1+pAnh5gW5Vw=="
    a = '1234567890008766'
    res = AESUtil.encryt(a, key, iv)
    print(res)
    # print(AESUtil.decrypt(res, key, iv))
    # t = base64.b64decode('0123456789abcdef')
    # AES_CBC_decrypt(a,t,t)


    '''
    BBqFfuM0L8HSdPIjp7baELTTmCcJHl
    
    '''