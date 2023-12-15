from flask import Flask, request, jsonify, render_template
import scrapingsel  # This is your scraping module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # You will create this HTML file for input

@app.route('/scrape', methods=['POST'])
def scrape():
    conference = request.form.get('conference')
    keywords = request.form.get('keywords').split(',')
    results = scrapingsel.scrape_papers(conference, keywords)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)