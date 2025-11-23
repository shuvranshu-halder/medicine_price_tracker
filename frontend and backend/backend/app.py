from flask import Flask, jsonify,request,send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
from flask_cors import CORS
from tata1mg_scrape import scrape_tata1mg
from pharmeasy import scrape_pharmeasy
from netmeds import get_medicine_price
from apollo import scrape_apollo
from database import get_db,init_db,save_search
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# dictionary cache
CACHE = {}
CACHE_EXPIRY = timedelta(hours=1)
combined={}

def get_cached_result(medicine):
    medicine = medicine.lower().strip()
    if medicine not in CACHE:
        return None

    cached_time = CACHE[medicine]["timestamp"]
    if datetime.now() - cached_time > CACHE_EXPIRY:
        return None  # cache expired

    return CACHE[medicine]["data"]

def save_cache(medicine, data):
    CACHE[medicine.lower().strip()] = {
        "timestamp": datetime.now(),
        "data": data
    }

@app.get("/check_cache")
def check_cache():
    medicine = request.args.get("medicine", "").strip()

    cached = get_cached_result(medicine)
    if cached:
        print("Serving from cache")
        return jsonify({"cached": True, "data": cached})
    else:
        return jsonify({"cached": False})
    
@app.post("/save-full-cache")
def save_full_cache():
    data = request.json
    medicine = data["medicine"]
    results = data["results"]

    save_cache(medicine, results)
    return {"status": "cached"}

#-----------------------------------------

@app.post("/start-search")
def start_search():
    data = request.json
    medicine = data.get("medicine")

    if medicine:
        save_search(medicine) 

    return {"status": "ok"}

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

@app.post("/download-pdf")
def download_pdf():
    data = request.json
    medicine = data.get("medicine", "Medicine")
    results = data.get("results", {})

    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    body_style = styles["BodyText"]
    body_style.wordWrap = "CJK"  # 🔥 enables line wrapping

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    elements = []

    # Title
    elements.append(Paragraph(f"<b>Price Comparison for: {medicine}</b>", title_style))
    elements.append(Spacer(1, 12))

    for site, site_results in results.items():
        elements.append(Paragraph(f"<b>{site}</b>", styles["Heading2"]))
        elements.append(Spacer(1, 6))

        if not site_results:
            elements.append(Paragraph("No data found.", styles["BodyText"]))
            elements.append(Spacer(1, 12))
            continue

        # Table header
        def to_str(value):
            if value is None:
                return "-"
            return str(value)

        data_table = [
            [
                Paragraph("<b>Name</b>", body_style),
                Paragraph("<b>MRP</b>", body_style),
                Paragraph("<b>Selling Price</b>", body_style),
            ]
        ]

        for item in site_results:
            data_table.append([
                Paragraph(to_str(item.get("name", "-")), body_style),
                Paragraph(to_str(item.get("MRP", "-")), body_style),
                Paragraph(to_str(item.get("selling_price", "-")), body_style),
            ])


        # Create table (column width adjusted so long text wraps)
        table = Table(data_table, colWidths=[230, 80, 100])

        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),

            ('ALIGN', (1,1), (-1,-1), 'CENTER'),

            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),

            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('TOPPADDING', (0,0), (-1,0), 8),

            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

    pdf.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="medicine_prices.pdf")

@app.get("/get-count")
def get_count():
    medicine = request.args.get("medicine")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT count FROM searches WHERE name = ?", (medicine,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return {"count": row["count"]}
    else:
        return {"count": 0}

if __name__=="__main__":
    init_db()
    app.run(debug=True)
    