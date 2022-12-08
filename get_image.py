import requests
import json

URL = 'https://api.pexels.com/v1/search?query='
HEADERS = {'Authorization': '563492ad6f9170000100000149f33d28a2c64d898caf9e9f10923cfa'}
























































def get_image_href(query):
    r = requests.get(URL+query, headers=HEADERS)

    r_obj = json.loads(r.text)
    #print(r_obj["photos"][0]["url"])
    return r_obj["photos"][0]["src"]["original"]

if __name__ == '__main__':
    print(get_image_href("google"))