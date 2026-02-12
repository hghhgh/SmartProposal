import hvac
from fastapi import HTTPException

# اتصال به Vault
client = hvac.Client(url="http://127.0.0.1:8200", token="")

def get_secret(key_name: str):
    try:
        secret = client.secrets.kv.v2.read_secret_version(path=key_name)
        return secret["data"]["data"]
    except hvac.exceptions.InvalidPath:
        raise HTTPException(status_code=404, detail="Key not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def set_secret(key_name: str, value: str):
    try:
        client.secrets.kv.v2.create_or_update_secret(path=key_name, secret={"value": value})
        return {"msg": f"Key '{key_name}' stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
