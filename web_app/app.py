from flask import Flask, request
from flask import send_file,session,jsonify

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



if __name__ == "__main__":
    app.run()
