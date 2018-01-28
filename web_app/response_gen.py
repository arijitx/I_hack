import json
import random
import requests
import pymongo

class ResponseBuilder():
    def __init__(self):
        self.utter_map=json.load(open('utter.json'))
        self.orders={}

    def utter(self,action):
        responses=self.utter_map[action]
        idx=random.randint(0,len(responses)-1)
        return responses[idx]

    def action_search_restaurants(self,slots):
        print(slots)
        location=slots['location']
        cuisine=slots['cuisine']
        r=requests.get('https://developers.zomato.com/api/v2.1/locations?query='+location,headers={'user-key': 'fb627d5a1d8b3431f8b260310bbad9a6'})
        print(r.json())
        entity_id=r.json()['location_suggestions'][0]['entity_id']
        entity_type=r.json()['location_suggestions'][0]['entity_type']
        url='https://developers.zomato.com/api/v2.1/search?entity_id='+str(entity_id)+'&cuisines='+cuisine+'&entity_type='+entity_type
        r=requests.get(url,headers={'user-key': 'fb627d5a1d8b3431f8b260310bbad9a6'}).json()
        info=[]
        for rx in r['restaurants'][:3]:
            info.append(rx['restaurant']['name'])
            info.append(rx['restaurant']['user_rating']['aggregate_rating'])
            info.append(rx['restaurant']['url'])
        slider='<div class="well"><div id="myCarousel" class="carousel slide"><div class="carousel-inner"><div class="item active"><div class="row-fluid"><h3>{}</h3><h1>{}</h1><div class="span3"><a target="_blank" href={}><button  type="button" class="btn btn-success">Go</button></a></div></div></div><div class="item"><div class="row-fluid"><h3>{}</h3><h1>{}</h1><div class="span3"><a target="_blank" href={}><button  type="button" class="btn btn-success">Go</button></a></div></div></div><div class="item"><div class="row-fluid"><h3>{}</h3><h1>{}</h1><div class="span3"><a target="_blank" href={}><button  type="button" class="btn btn-success">Go</button></a></div></div></div><a class="left carousel-control" href="#myCarousel" data-slide="prev">‹</a><a class="right carousel-control" href="#myCarousel" data-slide="next">›</a></div></div>'.format(*info)
        return slider

    def action_placeorder(self,slots,msg,u_name):
        foods=[]
        for e in msg['entities']:
            if(e['entity']=='food'):
                foods.append(e['value'])
        self.orders[u_name]=foods
        return self.utter("utter_placeorder")

    def action_repeatorder(self,slots,msg,u_name):
        if(u_name in self.orders):
            last_order=self.orders[u_name]
            resp="<ol>"
            for i in last_order:
                resp+="<li>"+i+"</li>"
            resp+='</ol><br>'
            return resp+self.utter("utter_repeatorder")
        else:
            return "Looks like you don't have any past orders . X( "

    def action_addtoorder(self,slots,msg,u_name):
        if(u_name in self.orders):
            new_foods=[]
            for e in msg['entities']:
                if(e['entity']=='food'):
                    new_foods.append(e['value'])
            last_order=self.orders[u_name]
            order=last_order+new_foods
            self.orders[u_name]=order
            resp="<ol>"
            for i in order:
                resp+="<li>"+i+"</li>"
            resp+='</ol><br>'
            return resp+self.utter("utter_addtoorder")
        else:
            return "Looks like you don't have any past orders . X( "
