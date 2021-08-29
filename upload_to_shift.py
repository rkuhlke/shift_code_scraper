import bs4
import requests


class Upload2Shift:
    def __init__(self, username, password):
        self.username = username
        self.password = password    
        def connect(self):
            headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
            session = requests.session()
            agent = session.get("https://shift.gearboxsoftware.com/home")
            token = getCSRFToken(agent.text)
            data = {"authenticity_token": token, "user[email]": username, "user[password]": password, "commit": "SIGN IN", "redirect_to": "https://shift.gearboxsoftware.com/rewards"}
            session.post("https://shift.gearboxsoftware.com/sessions", data=data, headers=headers)
            return session
        self.session = connect(self)
    
    def uploadCode(self, item):
        resp1 = self.session.get("https://shift.gearboxsoftware.com/rewards")
        token = getCSRFToken(resp1.text)
        print(token)
        code = item.get("archive:shift").get("shift:code")
        service = item.get("archive:shift").get("shift:platform")
        print(service)
        if service.lower() == "universal":
            servicelist = ["steam", "xboxlive"]
            for service in servicelist:
                data = {
                    "authenticity_token": token,
                    "archway_code_redemption[code]": code,
                    "archway_code_redemption[service]": service
                }
                resp = self.session.post("https://shift.gearboxsoftware.com/code_redemptions", data=data)
                print(resp.status_code)
    

def getCSRFToken(text):
    soup = bs4.BeautifulSoup(text, "html.parser")
    token = soup.find("meta", {"name": "csrf-token"})["content"]
    return token