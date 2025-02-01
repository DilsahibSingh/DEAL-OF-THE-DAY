from flask import Flask, render_template, jsonify
from flask_apscheduler.scheduler import APScheduler
import json
from webscraper.amazon_scraper import scrape_products

app = Flask(__name__)
scheduler = APScheduler()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# API to Fetch Current Deals
@app.route('/get_deals', methods=['GET'])
def get_deals():
    try:
        with open('db.json', 'r') as file:
            deals = json.load(file)
        return jsonify(deals)
    except:
        return jsonify([])  

# API to Manually Load More Deals
@app.route('/load_more', methods=['GET'])
def load_more():
    new_deals = scrape_products() 
    return jsonify(new_deals) 

# Background Task: Auto-Scrape Deals Every Hour
def auto_update_deals():
    print("🔄 Running scheduled deal update...")
    scrape_products()

# Schedule Task to Run Every 1 Hour
scheduler.add_job(id="Auto Scraper", func=auto_update_deals, trigger="interval", minutes=60)

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)
