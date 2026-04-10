from pprint import pprint

from bs4 import BeautifulSoup

from clients.core import Client

# https://portaleps.epssura.com/TramitesUnClickNet/api/AfiliacionesService/ConsultarDatosAfiliado
# https://seus.suramericana.com/idp/login/client/sso
# https://login.sura.com/sso/servicelogin.aspx?continueTo=https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F&service=epssura
# https://seus.suramericana.com/idp/client/login
# https://login.sura.com/sso/servicelogin.aspx?continueTo=https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F&service=epssura


def sso_login(client: Client, document: int, password: str):
    """
    Login to the portal using the document and password
    Args:
        document: int
        password: str
    Returns:
        None
    """

    # step 1, go to sites and refresh cookies.add(element)
    client.session.get(
        "https://portaleps.epssura.com/TramitesUnClickNet/api/AfiliacionesService/ConsultarDatosAfiliado"
    )
    client.session.get("https://seus.suramericana.com/idp/login/client/sso")
    client.session.get(
        "https://login.sura.com/sso/servicelogin.aspx?continueTo=https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F&service=epssura"
    )
    client.session.get("https://seus.suramericana.com/idp/client/login")
    client.session.get(
        "https://login.sura.com/sso/servicelogin.aspx?continueTo=https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F&service=epssura"
    )

    # step 2, https://portaleps.epssura.com/TramitesUnClickNet/api/AfiliacionesService/ConsultarDatosAfiliado, get SAML: <input type='hidden' name='SAMLRequest' value='
    tramites_un_click_response = client.session.get(
        "https://portaleps.epssura.com/TramitesUnClickNet/api/AfiliacionesService/ConsultarDatosAfiliado"
    )

    soup = BeautifulSoup(tramites_un_click_response.text, "html.parser")
    saml: str = soup.find("input", {"name": "SAMLRequest"}).get("value")
    pprint(f"saml: {saml}")
    relay_state: str = soup.find("input", {"name": "RelayState"}).get("value")
    pprint(f"relay_state: {relay_state}")

    # step 3, https://seus.suramericana.com/idp/login/client/sso, POST extracted SAML: <input type='hidden' name='SAMLRequest' value='
    seus_sso_response = client.session.post(
        "https://seus.suramericana.com/idp/login/client/sso", data={"SAMLRequest": saml}
    )
    soup = BeautifulSoup(seus_sso_response.text, "html.parser")
    req_id: str = soup.find("input", {"name": "reqID"}).get("value")

    response = client.session.post(
        "https://seus.suramericana.com/idp/login/client/sso",
        data={"SAMLRequest": saml, "RelayState": relay_state},
    )
    # nothing to do here

    # step 4, https://login.sura.com/sso/servicelogin.aspx?continueTo=https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F&service=epssura, POST extracted SAML: <input type='hidden' name='SAMLRequest' value='
    sura_service_login_response = client.session.post(
        "https://login.sura.com/sso/servicelogin.aspx?continueTo=https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F&service=epssura",
        data={
            "spEntityId": "portalEPSAfiliados",
            "username": document,
            "password": password,
            "service": "epssura",
            "reqID": req_id,
            "continueTo": "https://portaleps.epssura.com/ServiciosUnClick/",
            "country": "CO",
            "acsURL": "https://seus.epssura.com/acs/acs",
            "idpId": "2",
            "tag": "PORTALES",
        },
    )

    pprint(
        {
            "username": document,
            "password": password,
            "spEntityId": "portalEPSAfiliados",
            "service": "epssura",
            "reqID": req_id,
            "continueTo": "https%3A%2F%2Fportaleps.epssura.com%2FServiciosUnClick%2F",
            "country": "CO",
            "acsURL": "https%3A%2F%2Fseus.epssura.com%2Facs%2Facs",
            "idpId": "2",
            "tag": "PORTALES",
        }
    )

    return client
