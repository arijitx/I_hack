from flask import Flask, request
from flask import send_file,session,jsonify
import requests
from response_gen import ResponseBuilder

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.secret_key = 'chatapp'

@app.route('/')
def root():
    if 'u_name' not in session:
        return send_file('index.html')
    else:
        return send_file('chat.html')

@app.route('/save_user', methods=['GET', 'POST'])
def save_user():
    u_name=request.args.get('u_name')
    session['u_name']=u_name
    return jsonify("{'status':'success'}")

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    del session['u_name']
    return "logout"

@app.route('/chat',methods=['GET', 'POST'])
def chat():
    msg=request.args.get('msg')
    m_type=request.args.get('type')
    print('chat->',m_type)
    response={}
    # if 'place' in msg or 'order' in msg or 'addtoorder' in msg or 'placeorder' in msg or 'repeatorder' in msg :
    #     if(m_type == 'normal'):
    #         url='http://localhost:5006/conversations/'+session['u_name']+'/parse?q='
    #     else:
    #         url='http://localhost:5006/conversations/'+session['u_name']+'/continue'
    # else:
    #     if(m_type == 'normal'):
    #         url='http://localhost:5005/conversations/'+session['u_name']+'/parse?q='
    #     else:
    #         url='http://localhost:5005/conversations/'+session['u_name']+'/continue'
    if(m_type == 'normal'):
        url='http://localhost:5005/conversations/'+session['u_name']+'/parse?q='
    else:
        url='http://localhost:5005/conversations/'+session['u_name']+'/continue'
    if(m_type=='normal'):
        r = requests.get(url+msg)
    else:
        post_data={"executed_action": msg, "events": []}
        r = requests.post(url,json=post_data)
    if "action_suggest"==r.json()['next_action']:
        response['action']="action_listen"
    else:
        response['action']=r.json()['next_action']
    response['response']=action_to_string(response['action'],r.json()['tracker']['slots'],r.json()['tracker']['latest_message'])
    return jsonify(response)

def action_to_string(action,slots,msg):
    print(action)
    if action=='utter_placeorder':
        return rb.action_placeorder(slots,msg,session['u_name'])
    if action=='utter_repeatorder':
        return rb.action_repeatorder(slots,msg,session['u_name'])
    if action=='utter_addtoorder':
        return rb.action_addtoorder(slots,msg,session['u_name'])

    if 'action_listen'==action:
        return "action_listen"
    if 'utter' in action:
        return rb.utter(action)
    if 'action' in action:
        if(action=='action_search_restaurants'):
            return rb.action_search_restaurants(slots)
        if(action=='action_suggest'):
            return "action_listen"

    return ""


if __name__ == "__main__":
    rb=ResponseBuilder()
    app.run(host= '0.0.0.0')
