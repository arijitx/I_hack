import json
import random
import requests

class ResponseBuilder():
    def __init__(self):
        self.utter_map=json.load(open('utter.json'))

    def utter(self,action):
        responses=lf.utter_map[utter]
        idx=random.randint(0,len(responses)-1)
        return responses[idx]

    def action_factory(self,slots):
        location=slots['city']
        cuisine=slots['cuisine']
        r=requests.get('https://developers.zomato.com/api/v2.1/locations?query='+location,headers={'user-key': 'fb627d5a1d8b3431f8b260310bbad9a6'})
        print(r.json())
        entity_id=r.json()['location_suggestions'][0]['entity_id']
        url='https://developers.zomato.com/api/v2.1/search?entity_id='+str(entity_id)+'&cuisines='+cuisines
        r=requests.get(url,headers={'user-key': 'fb627d5a1d8b3431f8b260310bbad9a6'})
        response="<ul>"
        for rx in r['restaurants']:
            response+="<li>"+rx['name']+'</li>'
        response+="</ul>"
        return response
