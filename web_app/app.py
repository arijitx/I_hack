from flask import Flask, request
from flask import send_file,session,jsonify
import requests

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

@app.route('/chat',methods=['GET', 'POST'])
def chat():
    msg=request.args.get('msg')
    m_type=request.args.get('type')
    print('chat->',m_type)
    response={}
    if(m_type == 'normal'):
        url='http://localhost:5005/conversations/'+session['u_name']+'/parse?q='
    else:
        url='http://localhost:5005/conversations/'+session['u_name']+'/continue'
    if(m_type=='normal'):
        r = requests.get(url+msg)
    else:
        post_data={"executed_action": msg, "events": []}
        r = requests.post(url,json=post_data)

    response['action']=r.json()['next_action']
    response['response']=action_to_string(response['action'])
    return jsonify(response)

def action_to_string(action):
    if 'utter' in action:


if __name__ == "__main__":
    app.run()
