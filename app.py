from flask import Flask, request, render_template_string, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import xlwt
from xlwt import Workbook

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = None
    if request.method == 'POST':
        url = request.form['url']
        if url:
            images, links = get_all_links_and_images(url)
            data = {
                'images': images,
                'links': links
            }
    return render_template_string(form_template, data=data)

@app.route('/get_link', methods=['GET'])
def get_link():
    # Get the URL from the query parameters
    url = request.args.get('url')
    
    # Check if URL is provided
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
   
    images, links = get_all_links_and_images(url)
      
    # Use jsonify to convert the dictionary to a JSON response
    data = {
        'images': images,
        'links': links
    }
    return jsonify(data), 200

# Function to scrape all href links and image URLs
def get_all_links_and_images(url):
    # Set up the WebDriver with headless option
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    driver.implicitly_wait(10)

    # Workbook creation
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'Images')
    sheet1.write(0, 1, 'Links')

    try:
        # Find all anchor tags on the page
        anchor_tags = driver.find_elements(By.TAG_NAME, 'a')
        # Find all image tags on the page
        image_tags = driver.find_elements(By.TAG_NAME, 'img')

        # Extract the href attribute from each anchor tag
        links = [anchor.get_attribute('href') for anchor in anchor_tags if anchor.get_attribute('href')]

        # Extract the src attribute from each image tag
        images = [img.get_attribute('src') for img in image_tags if img.get_attribute('src')]

        # Write to the Excel sheet
        for index, link in enumerate(links, start=1):
            sheet1.write(index, 1, link)

        for index, img in enumerate(images, start=1):
            sheet1.write(index, 0, img)

        wb.save('xlwt_example.xls')
        return images, links
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []
    finally:
        driver.quit()

form_template = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Input Form</title>
</head>
<body>
    <h1>Enter URL to Scrape</h1>
    <form method="POST">
        <input type="text" name="url" required>
        <input type="submit" value="Submit">
    </form>
    {% if data %}
        <h2>Scraped Data</h2>
        <h3>Links</h3>
        <ul>
            {% for link in data.links %}
                <li><a href="{{ link }}" target="_blank">{{ link }}</a></li>
            {% endfor %}
        </ul>
        <h3>Images</h3>
        <ul>
            {% for img in data.images %}
                <li><img src="{{ img }}" alt="Image" style="max-width: 200px;"></li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
