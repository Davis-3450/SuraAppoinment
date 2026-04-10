from httpx import Client

from clients.auth import sso_login

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Sec-Ch-Ua-Platform": "Windows",
    "Accept-Language": "en-US,en;q=0.9",
    # "X-Dtpc": "6$374847996_725h6vOKGCEWCRRCUSUOPPJJMKAUFRBBHJUHSA-0e0",
    "Sec-Ch-Ua": '"Not-A.Brand";v="24", "Chromium";v="146"',
    "Sec-Ch-Ua-Mobile": "?0",
    "X-App-Relaystate": "https://portaleps.epssura.com/ServiciosUnClick/#/",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://portaleps.epssura.com",
    "Sec-Fetch-Site": "same-origin",
}


#  Content-Length: 0
# Sec-Ch-Ua-Platform: "Windows"
# Accept-Language: en-US,en;q=0.9
# X-Dtpc: 6$374847996_725h6vOKGCEWCRRCUSUOPPJJMKAUFRBBHJUHSA-0e0
# Sec-Ch-Ua: "Not-A.Brand";v="24", "Chromium";v="146"
# Sec-Ch-Ua-Mobile: ?0
# X-App-Relaystate: https://portaleps.epssura.com/ServiciosUnClick/#/
# Accept: application/json, text/plain, */*
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36
# Origin: https://portaleps.epssura.com
# Sec-Fetch-Site: same-origin
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://portaleps.epssura.com/ServiciosUnClick/
# Accept-Encoding: gzip, deflate, br
# Priority: u=1, i
# Connection: keep-alive


class ClientHTTP:
    def __init__(self):
        self.session = Client()
        self.session.headers.update(HEADERS)

    def login(self, document: int, password: str):
        """
        Login to the portal using the document and password
        Args:
            document: str
            password: str
        Returns:
            None
        """
        doc: str = "C" + str(document).zfill(8)
        return sso_login(self, doc, password)


client = Client()  # global client
