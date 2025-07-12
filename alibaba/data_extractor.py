# imported all necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
from datetime import datetime

# creating a file for saving the extraced data
file_name='alibaba.csv'

# function for saving the data 
def save_data(df):

    try:
        if os.path.exists(file_name):
            existing = pd.read_csv(file_name)
            df = pd.concat([existing, df], ignore_index=True)
        df.to_csv(file_name,index=False)
    except Exception as e:
        print(f'Error saving data: {e}') 

# link of alibaba.com
# url for UAE 
url="https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"
# url for all RFQ
# url="https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677538.2.715065aaBa9KrK"

# launching of the chrome web browser
driver=webdriver.Chrome()

def extract_data(url):
    # scraping alibaba.com
    driver.get(url)

    # extracting the title 
    # using try except by which the rest of the code still runs if it gives error 
    try:
        title1=driver.find_elements(By.CLASS_NAME,"brh-rfq-item__subject-link")
        title=title1[0].text
        url1=title1[0].get_attribute("href")
        print(url1)
        print(title)
        time.sleep(2)
    except:
        print("Title not found")    

    # extracting the buyer name and buyer image
    try:
        buyer=driver.find_elements(By.CLASS_NAME,"text")
        print('buyer')
        print(buyer[0].text)
        buyer_name=buyer[0].text
    
        buyer_img=driver.find_elements(By.CLASS_NAME,"default-img")
        print("buyer_img",buyer_img[0].get_attribute("src"))
        buyer_image=buyer_img[0].get_attribute("src")
    except:
        print("Buyer and img not found")
    
    # extracting Date posted
    try:
        enquiry_time=driver.find_elements(By.XPATH,"//div[@class='brh-rfq-item__publishtime']")
        full_text=enquiry_time[0].text.strip()
        time_info=full_text.split(":")[-1].strip()
        print("date posted",time_info)

    except:
        print("inquiry time not found")

    # extracting quotes left
    try:    
        quotes_left=driver.find_elements(By.XPATH,"//div[@class='brh-rfq-item__quote-left']//span[1]")
        print("Quote left",quotes_left[0].text)
        quotes=quotes_left[0].text

    except:
        print("item left not found")

    # extracting country name
    try:
        country_div = driver.find_elements(By.CLASS_NAME, "brh-rfq-item__country")
        full_text1 = country_div[0].text.strip()
        country=full_text1.split(":")[-1].strip()
        print("country",country)
    except:
        print("country not found")
    
    # extracting quantity required
    try:
        quantity_req=driver.find_elements(By.CLASS_NAME,"brh-rfq-item__quantity-num")
        print("quantity req",quantity_req[0].text)
        quantity_required=quantity_req[0].text
    except:
        print("quantity required not found")

    # extracting email confirmation 
    try:   
    # initializing the values so that garbage value error wont occur 
        email="No"
        experience="No"
        interactive="No"
        replies="No"
        rfq="No"

    # Locate the parent div using its class
        parent_div = driver.find_element(By.CLASS_NAME, "bc-brh-rfq-flag--buyer")

    # Find all child tags under the parent div  
        tags = parent_div.find_elements(By.CLASS_NAME, "next-tag-body")

    # Extract text from each tag
        labels = [tag.text.strip() for tag in tags]

        for i in labels:
            print(i)
            if i == "Email Confirmed":
                email = "Yes"
            elif i == "Experienced buyer":
                experience = "Yes"
            elif i == 'Interactive replies':
                interactive = "Yes"
            elif i == 'Typically replies':
                replies = "Yes"
            elif i == "Complete order via RFQ":
                rfq = "Yes"
    except:
        print("Email confirmed not found")

    # extracting the date posted using the url of title
    try:
        driver.get(url1)
        date_posted=driver.find_element(By.CLASS_NAME,"datetime")
        date__=date_posted.text.strip()
        date=date__.split(":")[0]
        print(date)
    except:
        print("url not found")
    # scraping date using now function 
    date=datetime.now()
    scratch_date=date.strftime("%d-%m-%Y")
    
    # loading data and creating columns for aligning the data 
    data=pd.DataFrame([[title,buyer_name,buyer_image,time_info,quotes,country,quantity_required,email,experience,interactive,replies,rfq,url1,date,scratch_date]],columns=['TItle','Buyer_name','Buyer_image','Date Posted','Quotes left','Country','Quantity Required','Email Confirmation',"Experienced buyer","Interctive User","Typically Replies","Complete Order via RFQ","Inquiry email","Inquiry date","Scratch Date"])
    trends=data.dropna(axis=1,how='all')
    # saving to the csv file which we created earlier
    save_data(trends)
    print("data saved successfully")

# calling the function to extract the data
if __name__=='__main__':
    extract_data(url)
    driver.quit()
