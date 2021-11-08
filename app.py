from flask import Flask,request
import json
import random
import string
app = Flask(__name__)

root_url = "http://infra.io/"
CONFIG_FILE = r'config.json'

def read_json_file(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data
    
def write_to_json_file(json_data,json_file):
    with open(json_file, 'w') as json_file:
        json.dump(json_data, json_file)
        
def encode_string():
    ascii_letters = string.ascii_lowercase + string.ascii_uppercase
    letters = random.choices(ascii_letters, k=3)
    encode_letters = "".join(letters)
    return encode_letters

def shorten_url(url):
    short_urls = read_json_file(CONFIG_FILE)
    if short_urls:
        while True:
            encode_letters = encode_string()
            if url in short_urls.keys():
                return short_urls[url]
            elif encode_letters not in short_urls.values():
                short_urls[url]=encode_letters
                write_to_json_file(short_urls,CONFIG_FILE)
                return short_urls[url]
    else:
        encode_letters = encode_string()
        short_urls[url]=encode_letters
        write_to_json_file(short_urls,CONFIG_FILE)
        return encode_letters


@app.route('/', methods=['GET'])
def tiny_url():
     url = request.args.get("url")
     if url:
        hyper = shorten_url(url)
        if hyper:
            return root_url+hyper
     else:
        return f'<h1>query parameter is invalid or not found</h1>'


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')