from flask import Flask, jsonify,request
from flask_cors import CORS
from tata1mg_scrape import scrape_tata1mg
from pharmeasy import scrape_pharmeasy
from netmeds import get_medicine_price
from apollo import scrape_apollo
app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def home():
    return "Welcome to the Medicine Price Tracker API."

@app.route('/tata1mg', methods=['GET'])
def get_price():

    medicine_name = request.args.get('medicine_name')
    tata1mg_price_info = scrape_tata1mg(medicine_name)
    
    return jsonify(tata1mg_price_info)

@app.route('/pharmeasy', methods=['GET'])
def PE_get_price():

    medicine_name = request.args.get('medicine_name')
    pharmeasy_price_info = scrape_pharmeasy(medicine_name)
    
    return jsonify(pharmeasy_price_info)

@app.route('/netmeds', methods=['GET'])
def NM_get_price():

    medicine_name = request.args.get('medicine_name')
    netmeds_price_info = get_medicine_price(medicine_name)
    
    return jsonify(netmeds_price_info)

@app.route('/apollo', methods=['GET'])
def AP_get_price():

    medicine_name = request.args.get('medicine_name')
    AP_price_info = scrape_apollo(medicine_name)
    
    return jsonify(AP_price_info)

if __name__=="__main__":
    app.run(debug=True)