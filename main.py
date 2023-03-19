from flask import Flask, jsonify, request
from tools import retrieve_info
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):

        data = "hello world"
        return jsonify({'data': data})

@app.route('/get_info', methods = ['GET'])
def disp():
    print(request.args)
    data = retrieve_info(request.args.get("url"))
    
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=43)