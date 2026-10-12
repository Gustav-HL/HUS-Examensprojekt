import os
from urllib.parse import quote
import httpx
from dotenv import load_dotenv
import msal

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SHAREPOINT_HOSTNAME = os.getenv("SHAREPOINT_HOSTNAME", "susearch.sharepoint.com")
FILE_PATH = os.getenv("FILE_PATH", "download.pdf")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]


def get_access_token():
    """Hämtar en access-token från Microsoft Entra ID."""
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )
    result = msal_app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        return result["access_token"]
    else:
        error_desc = result.get("error_description", "Kunde inte hämta token")
        raise Exception(f"Autentiseringsfel: {error_desc}")


def get_file_metadata():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    drive_lookup_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOSTNAME}/drive"
    print(f"Drive ID URL: {drive_lookup_url}")

    drive_response = httpx.get(drive_lookup_url, headers=headers)

    if drive_response.status_code != 200:
        print(f"Fel vid hämtning av Drive ID ({drive_response.status_code}): {drive_response.text}")
        return

    drive_data = drive_response.json()
    drive_id = drive_data.get("id")
    print(f"Drive ID: {drive_id}")

    clean_file_path = FILE_PATH.strip("/")
    encoded_file_path = quote(clean_file_path, safe="/")

    file_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{encoded_file_path}"
    print(f"Fil URL: {file_url}")

    file_response = httpx.get(file_url, headers=headers)


    if file_response.status_code == 200:
        data = file_response.json()
        print("\n Metadata:")
        
        import json
        print(json.dumps(data, indent=4))
        
        fields = data.get("listItem", {}).get("fields", {})
        for key, value in fields.items():
            print(f"  {key}: {value}")


    else:
        print(f"\n Fel vid hämtning av fil ({file_response.status_code}): {file_response.text}")

get_file_metadata()