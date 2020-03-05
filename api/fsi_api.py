from nibss.credentials import Credentials
from nibss.bvn import Bvn

YOUR_ORGANIZATION_CODE = "11111"
YOUR_SANDBOX_KEY = "f089e1189acb8419fcff28bc6d2177a0"

header = {
    "base_url": "",
    "Organizationcode": YOUR_ORGANIZATION_CODE,
    "sandbox-key": YOUR_SANDBOX_KEY,
    "content-type": "application/json",
    "accept": "application/json",
    "username": YOUR_ORGANIZATION_CODE,
    "password": "",
}

reset = Credentials(header).reset()

YOUR_PASSWORD = header["password"] = reset['password']
YOUR_AES_KEY = reset['aes_key']
YOUR_IV_KEY = reset['ivkey']

verify_single = Bvn(header).verify_single({
    "body": {"BVN": "12345678901"},
    "Aes_key": YOUR_AES_KEY,
    "Iv_key": YOUR_IV_KEY
})

print(verify_single)
