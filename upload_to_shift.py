import bs4
import requests

base_url = "https://shift.gearboxsoftware.com"

class Upload2Shift:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.connect()
    
    def connect(self):
            agent = self.session.get(f"{base_url}/home")
            token = getCSRFToken(agent.text)
            data = {"authenticity_token": token, "user[email]": self.username, "user[password]": self.password}
            headers = {"Referer": f"{base_url}/home"}
            self.session.post(f"{base_url}/sessions", data=data, headers=headers)
    
    def uploadCode(self, code):
        resp = self.session.get(f"{base_url}/rewards")
        token = getCSRFToken(resp.text)
        headers = {
            "x-requested-with": "XMLHttpRequest",
            "x-csrf-token": token
            }
        resp2 = self.session.get(f"{base_url}/entitlement_offer_codes?code={code}", headers=headers)
        soup = bs4.BeautifulSoup(resp2.text, "html.parser")
        forms = soup.find_all("form")
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
            self.session.post(f"{base_url}/code_redemptions", data=data, headers=post_headers)            
            

def getCSRFToken(text):
    soup = bs4.BeautifulSoup(text, "html.parser")
    token = soup.find("meta", {"name": "csrf-token"})["content"]
    return token