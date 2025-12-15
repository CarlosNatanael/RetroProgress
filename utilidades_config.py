import keyring 
from keyring import errors as keyring_errors 

SERVICE_ID = "RetroProgress_RA_API" 

def save_credentials(username, api_key):
    """Salva as credenciais no armazenamento seguro do sistema."""
    keyring.set_password(SERVICE_ID, "ra_user", username) 
    keyring.set_password(SERVICE_ID, "ra_key", api_key)

def load_credentials():
    """Carrega as credenciais do armazenamento seguro."""
    username = keyring.get_password(SERVICE_ID, "ra_user")
    api_key = keyring.get_password(SERVICE_ID, "ra_key")
    return username, api_key

def clear_credentials():
    """Remove as credenciais do armazenamento seguro."""
    try:
        keyring.delete_password(SERVICE_ID, "ra_user")
    except keyring_errors.NoPasswordFound:
        pass
    try:
        keyring.delete_password(SERVICE_ID, "ra_key")
    except keyring_errors.NoPasswordFound:
        pass