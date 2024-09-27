import http.client
import json

class SerperTools:
    @staticmethod
    def scrape_and_summarize_website(query):
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': 'f95ceb5965c42a2b8e94f72e6e87bb0f502bb50e',
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8") 