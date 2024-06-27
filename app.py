from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import xlwt 
from xlwt import Workbook

app = Flask(__name__)


@app.route('/get_link', methods=['GET'])
def get_link():
    # Get the URL from the query parameters
    url = request.args.get('url')
    
    # Check if URL is provided
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
   
    images,links=get_all_links_and_images(url)
      
    # Use jsonify to convert the dictionary to a JSON response
    data = {
        'images': images,
         'links':links
    }
    return jsonify(data),200

# Function to scrape all href links and image URLs
def get_all_links_and_images(url):
     # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # URL of the target website
    # url = "https://sale-purchase.digitalisolutions.net/"
    # url="https://books.toscrape.com/"
    driver.get(url)

    # Implicit wait to allow the page to load
    driver.implicitly_wait(10)

    # Writing to an excel  
    # sheet using Python 

  
    # Workbook is created 
    wb = Workbook() 
  
    # add_sheet is used to create sheet. 
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
        
        print(f"Found {len(links)} links:")
        for index, link in enumerate(links, start=1):
            sheet1.write(index, 1,link) 
            print(link)
        
        # Print all found image URLs
        print(f"Found {len(images)} images:")
        for index, img in enumerate(images, start=1):
            sheet1.write(index, 0, img)
            print(img)

    
        wb.save('xlwt example.xls')
        return images,links
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        driver.quit()  

if __name__ == '__main__':
    app.run(debug=True)
    # Execute the function
    