import requests
# import time
from django.http import JsonResponse



cached_token = None

def get_mingle_token():
    global cached_token

    token_url = "https://mingle-sso.eu1.inforcloudsuite.com:443/LDE4VNS7C63W3JGC_DEM/as/token.oauth2"
    client_id = "LDE4VNS7C63W3JGC_DEM~AZOU1GoRHRJUSW9ek5U79lERXyrcEMzaQaBmNFm82fA"
    client_secret = "6oZIupwXdy5D2xswBxJchAM4kkPHlxNgn6hZch7_Ueq3AIZtlBOZVZF6l96DNqL5yb2pNXWgNVY-F23xNoxTtQ"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "password",
        "username": "LDE4VNS7C63W3JGC_DEM#MiEcMbq0duOOTfig-ZWlxpa574cFd9qJTVjXGIMj4oaR9JqEHHcacqgLln3AFDNn9uGe6wcgPuGWklHsQS-sdQ",
        "password": "ko5kvCJK_KD6Q0AimIFF0jO-OiKtatOZZF-qtavcTA-vG9Euc7eEcSfcV-tLJNo_eh45wybj-_vTwciSxI_sCw"
    }
    try:

        response = requests.post(token_url, headers=headers, data=data, auth=(client_id, client_secret))
        response.raise_for_status()
        token_data = response.json()
        cached_token = token_data["access_token"]
        # token_expiry = time.time() + token_data["expires_in"]
        return cached_token
    except Exception as e:
        print(f"❌ Token fetch failed: {e}")
        raise
