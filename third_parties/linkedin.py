import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        headers_dic = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        response = requests.get(api_endpoint,
                                params={"url": linkedin_profile_url},
                                headers=headers_dic,
                                timeout=10)
        
    data = response.json()

    # removing empty values
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], '', "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
        
if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/harshit-gupta-561543190/", mock=True
        )
    )