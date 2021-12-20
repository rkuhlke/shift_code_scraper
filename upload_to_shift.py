import bs4
import logging
import requests

base_url = "https://shift.gearboxsoftware.com"

class Upload2Shift:
    def __init__(self, username, password, logLevel=""):
        self.logger = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        if logLevel.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif logLevel.lower() == "error":
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)

        self.username = username
        self.password = password
        self.session = requests.session()
        self.__connect__()
            
    def __connect__(self):
        try:
            agent = self.session.get(f"{base_url}/home")
        except requests.RequestException as error:
            self.logger.error(f"Error: {error}")
        token = getCSRFToken(agent.text)
        data = {"authenticity_token": token, "user[email]": self.username, "user[password]": self.password}
        headers = {"Referer": f"{base_url}/home"}
        try:
            self.session.post(f"{base_url}/sessions", data=data, headers=headers)
        except requests.RequestException as error:
            self.logger.error(f"Error: {error}")
        self.logger.info("Successfully logged into Shift")
    
    def uploadCode(self, code):
        try:
            resp = self.session.get(f"{base_url}/rewards")
        except requests.RequestException as error:
            self.logger.error(f"Error: {error}")
        token = getCSRFToken(resp.text)
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "x-csrf-token": token
            }
        try:
            resp2 = self.session.get(f"{base_url}/entitlement_offer_codes?code={code}", headers=headers)
        except requests.RequestException as error:
            self.logger.error(f"Error: {error}")
        soup = bs4.BeautifulSoup(resp2.text, "html.parser")
        forms = soup.find_all("form")
        try:
            for form in forms:
                acr_code = form.find("input", {"name": "archway_code_redemption[code]"})["value"]
                acr_check = form.find("input", {"name": "archway_code_redemption[check]"})["value"]
                acr_service = form.find("input", {"name": "archway_code_redemption[service]"})["value"]
                acr_title = form.find("input", {"name": "archway_code_redemption[title]"})["value"]
                commit = form.find("input", {"name": "commit"})["value"]
                data = {
                    "authenticity_token": token,
                    "archway_code_redemption[code]": acr_code,
                    "archway_code_redemption[check]": acr_check,
                    "archway_code_redemption[service]": acr_service,
                    "archway_code_redemption[title]": acr_title,
                    "commit": commit
                }
                post_headers = {"Referer": f"{base_url}/new"}
                try:
                    self.session.post(f"{base_url}/code_redemptions", data=data, headers=post_headers)
                except requests.RequestException as error:
                    self.logger.error(f"Error: {error}")
                self.logger.info("Successfully Posted Code")
        except TypeError:
            self.logger.info("Code has been redeemed already")
        return         
            

def getCSRFToken(text):
    soup = bs4.BeautifulSoup(text, "html.parser")
    token = soup.find("meta", {"name": "csrf-token"})["content"]
    return token