from Cryptodome.Cipher import AES
import os
from Cryptodome import Random
import base64

"""
aes加密算法
padding : PKCS7
"""

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
    key = "0123456789abcdef"
    iv = b"0123456789abcdef"
    a = 'cE8v92iHlnVn wPi1XFT4EKpKeWz2lUbzQscQ5eziJkL8Ak8edIHGOZu jTq7jBB51SUlPbgNyvQAji3gA71WKgZPGVbDW6PchCkBFwy8klyhH9NH0RDbo5Qx5oNU4gnzoYSFwm0338dAZHPLZ5hjJVy2 71slk/IQTYMsvRT/KY//mJQq/9PXMP0ITOl7Ae6K9WYoPMdeTgABOef9LAZD5bTkn03s57W5PnPPRSOlkn C2Q6HcnuJzjsNNAHR5CQYuZVSrorDg4bnerJndCvQamH 1mBHcIh/GFyyKY8J1QAuYFaOlPaPZJwJ0pAtjhbTwcCOkAUTNLruXaRt7X/9nnLheJ1498OxEWv9uiqtid KIKIWNmDRIKt9nBu6GDhkEJBQL0KJ0BA85X0nj4CH8oyenN0ajgVTjMbdEpaaEyLPt7c 098Hh94yNMj93oJJDB5dY5fKQUtqhG2D0TTPc8wc0rcwFE8IMBty9RwD EPTUSDoxEen8oyenN0ajgtoAZvrGmvS7bvV5eznIulH8oyenN0ajgyGz5vz4WZ3c8y/eZS4ADlmS sk5EOsUWCqjBx IUnZqnwtCC6jS3xx44CecmT6wiC4i 61Kxb1Q5uNSv5FblUdZVjeZLYPHAeEu0uxMKPyfvMYfXiErT7PRp0l/KejFjdFiMhic/ue1jwRe3/ZdM0jDtH77LVLxewmZInBAFqAP1BR1Rw4jlk4S0MFZvvqJ7R4DFI6mWRa94S7S7Ewo/J 8xh9eIStPstNA8mUdPYAzKv5/eAohxrHLadZ8xTf31lq78yFF73A/PGrmnFj/PZmivyghR7IXoap4ePROuOsR9sojzJAkE14wPFqXZE3onR4DFI6mWRa KYSndoAgIHdMEdY2I8NyfakFltfOkoOsWfeTFdWkGMcdkW94e8MWBLHcXBLcf 0dORw48YkjwoJ29PbzA4y7OKDXyssQAPckqQPEEMTyZsgOS eK9idafWDPxdD OlbwwOfM3BMYDNdL77941bc4BS08VYT5TWq SR8hRu1ygodXnbym8ff/KZVi2 knW0OfS  /eNW3OAXMKryT4stIyJHKpiPG 3qQzngxEqqaU5ovznr0gf7Y14adST6VmHEnMini0/K2VZG5ljMRPqHHoOavyWbgteI gYrthp3oGtnuU5MHNy0RoV/XHLL012fEOz51iNJH3bWOe67PKvzbtchgNFIrn fdO49tiL2bgJaoXJW GhM/7MDtxRuxedNPiEQhJrNGTgerp2lKRuD4B3a eC CIHgY7htJ114HqVFToGdnm907Q653mjc9PcCjpbp6AoMIZsPp9x/0jiA/gfDYpHkZTRhW/8NdkGe7kClfFCcwMeTRypSjutAHnlweBUe5odL0AhSSU8YVm02nFaSDLdJQNtpsxaxhd662W dMjjDrCX5781SisbnKRvhq6haZ330tttKyTNr4roPqSqXgAO0CpPcEm0XMQWlTzc9IjOndrJQlRY8EXt/2XTNJ3o4U9MC1C4IrQ8ICflDbzwJqe3QyFYq3QimZS4TVakSId1bG4Gi6HbqY0eDs7B6vp0A9TSzc1DMbXzCwVLni3rVVTqK3o4rci4cZnQPeiTAEn6wivsXPsaVIhU1L2 cjruoF9 1dONak2z2QXi DgpIBX4lbdX01r m/o2qgn88i9Rs8YdnEXq15GbwpRZioPAw7GqjTsmAeHnA20UVqkMEvxo5R8ZEjKdlxG18IXRVYGeSTLBiX/9GiVnET KFkTeuFa9MX2gILQVR51MvYLhTk/TZQSil8m6HBdhhOKrmIrwaQaImUSQWQpQMBJaknJdDRRpcMQJCl0vrsc6TGzCU44bRp3bCqvImZMDQs rr2v2vG3eOdok9 e5QsfEow23oKGc6GFYI7DP5mbp/Eor8369aJTt1qqzI9uIyj6In7VlvSyjt862xzL9EUFI/CcNWVfVnxvS1qx0TOAScs23PNlMP EFLsUx2Q3Sqey1Ig11sKn5kceLV31pA4chww4tR3HTzvtgKfAdNECZL0NUIX/D5cF4NpADtZ fXsZkEmBZ7KG1YEABWIMLdxAvVxMTDriyDOpKMt12eRsFeRZP5YQxFGxEFO2EA6 0PcPwpLXeP1EyNy22YRZ7GjWyZWCeHkmndK3jlXN8z4ildhMRgsYOiYW7AA7EGO7jeuSmquBPnxhmqGQfsqpq5FE2extvNxDgR9ZTa8qqDrR0bmy WmCRtG5Z4hgteAf4TB8ANEINEwNdndCPLsWaVzLOwjjTtOUAwzzGEmBZ7KG1YEA1fWrSgTqFzImjdAm ZunpF5OIie6V/XwMZGQAlv9gET9dAEsOe9t4X8oyenN0ajgyHi zgjAK2vcEJ7f0rFI8ksj sbutfnO8m 40GTdkrPBMYwlDMZ8AlnbKmfjfVva5b4BvxTEgvUcjyyZZLaTcIuXv2 shgsvA2QW8tXZMGPJ16A Dn krvoFE8bLgwD0NoY65XtkOpa6FZrjZ603NxblPuZYf4e7kxYIeaeF8XtlPiM7UWN/J2hJmpUpc9zy6go9rBOT21L758tO24F8lOf1mf6hpWRRMCWZcJbsksYh4 x8CniZrlRHqHT1AqIAq4X iHMcQD8JTDJ6VY C7tRx5Jn9DCzJh3yw07bae3scA5clQm8VFi1oT6LvEChr PdM/dMPYlu7L/WX9VHnwUniVYcSn48T9LaJdnHyobJWV5mMbQOtQ4gNvnrTKksJ7bTbQ/yApru EjxS76ehEg=='

    res = AESUtil.encryt(a, key, iv)
    print(res)
    print(AESUtil.decrypt(res, key, iv))
    # t = base64.b64decode('0123456789abcdef')
    # AES_CBC_decrypt(a,t,t)


    '''
    BBqFfuM0L8HSdPIjp7baELTTmCcJHl
    
    '''