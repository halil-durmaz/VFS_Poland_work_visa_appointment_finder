############
# Libraries
############

# pandas
import pandas as pd                                                 # To extract personal data

# selenium
from selenium.webdriver import Chrome                               # Chromedriver
from selenium.webdriver.common.by import By                         # To find the elements
from selenium.webdriver.support.ui import WebDriverWait             # To wait
from selenium.webdriver.support import expected_conditions as EC    # To wait
from selenium.webdriver.chrome.options import Options               # To resize the chrome window
from selenium.common.exceptions import TimeoutException             # To apply try/except

# vlc
from vlc import MediaPlayer         # To run my music, when an appointment becomes available

# time (built-in)
from time import sleep              # To wait

# sys (built-in)
from sys import exit                # To stop the code









#############################################
# Extract sensitive data from the excel file
#############################################

df = pd.read_excel("Data.xlsx",
                   "Data",                          # Sheet name
                   index_col=0)                     # Set 1st column as row names


vfs_account_email = df.loc["VFS account e-mail"]['Value']
vfs_account_password = df.loc["VFS account password"]['Value']

first_name = df.loc["First name"]['Value']
last_name = df.loc["Last name"]['Value']
gender = df.loc["Gender"]['Value']
passport_number = df.loc["Passport number"]['Value']
country_calling_code = df.loc["Country calling code"]['Value']
phone_number = df.loc["Phone number"]['Value']
email = df.loc["E-mail"]['Value']








############################################
# Open a Chrome browser & Login to the page 
############################################

driver = Chrome()                                             # Create the Bot
driver.get("https://visa.vfsglobal.com/tur/en/pol/login")









###########################################################
# When Cookie panel becomes visible, close by accepting it
###########################################################

WebDriverWait(driver, 10) \
             .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                                "div#onetrust-button-group button#onetrust-accept-btn-handler"))) \
             .click()








##############################
# Enter the login information
##############################

driver.find_element(By.ID, "mat-input-0").send_keys(vfs_account_email)
driver.find_element(By.ID, "mat-input-1").send_keys(vfs_account_password)







##########################################
# Click to the Recaptcha button and solve
##########################################

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")))   # Write the title of the iframe that it is in. Because ReCaptcha checkbox is within an <iframe>
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()


# The user will manually solve Recaptcha here. Then, the code below will click on Sign In
sleep(12)                                                                      # Recaptcha can be easily solved within 12 seconds

driver.switch_to.default_content()                                             # To be able to switch between different Frames
WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-focus-indicator.btn.mat-btn-lg.btn-block.btn-brand-orange.mat-stroked-button.mat-button-base"))).click()








##########################
# Schedule an appointment
##########################

# If there is no slot for Istanbul region, return back to Dashboard; then try again (to be able to stay in the system)
for i in range(10000000000):         # We will check for 10000000000 times. This number is enough for 1 day
        try:
                #####################
                # Confirmations page
                #####################
                sleep(12) # Based on my experiments, 12 seconds should be enough
                
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(.//text(),'before scheduling')]"))).click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(.//text(), 'choose the correct' )]"))).click()

                driver.set_window_size(100, 700)     # When the page is narrowed by the sides, the location of the button is changing and finally the click operation works
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.mat-focus-indicator.btn.mat-btn-lg.btn-block.btn-brand-orange.mat-raised-button.mat-button-base"))).click()   # Button class içindeki yazıyı, boşlukları noktalarla değiştirerek yaz. Bekleme yapmadan da çalışmadı bu nedense, stackoverflow'da öyle çözmüş biri



                ############################
                # Terms and Conditions page
                ############################
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(.//text(), 'Continue Terms and Conditions' )]"))).click()                                                                                                     # Tıkladığında, inspect tarafında renklenen kısmın içindeki "id" değerini gir

                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.mat-focus-indicator.btn.mat-btn-lg.btn-block.btn-brand-orange.mat-stroked-button.mat-button-base"))).click()    # Button class içindeki yazıyı, boşlukları noktalarla değiştirerek yaz. Bekleme yapmadan da çalışmadı bu nedense, stackoverflow'da öyle çözmüş biri

                driver.maximize_window()      # To easily observe the future operations on the page, turn the window into the maximized version



                ####################
                # Your details page
                ####################
                sleep(2)         
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div/span[contains(., 'Select' )]"))).click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//mat-option/span[text()='" +gender+ "']"))).click()       # Because of the blank spaces at the start&end of the options of dropdown menu, this syntax is used

                sleep(2)          # If it does not wait for a while, it does not click to the next dropdown        
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div/span[contains(., 'Select' )]"))).click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//mat-option/span[contains(., 'Turkiye')]"))).click()

                # Since it created problems, I moved non-dropdown ones after the dropdown ones
                driver.find_element(By.XPATH, "//input[@placeholder='Enter your first name']").send_keys(first_name)
                driver.find_element(By.XPATH, "//input[@placeholder='Please enter last name.']").send_keys(last_name)
                driver.find_element(By.XPATH, "//input[@placeholder='Enter passport number']").send_keys(passport_number)
                driver.find_element(By.XPATH, "//input[@placeholder='44']").send_keys(country_calling_code)
                driver.find_element(By.XPATH, "//input[@placeholder='012345648382']").send_keys(phone_number)
                driver.find_element(By.XPATH, "//input[@placeholder='Enter Email Address']").send_keys(email)
            
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.mat-focus-indicator.mat-stroked-button.mat-button-base.btn.btn-block.btn-brand-orange.mat-btn-lg"))).click()      # Write the text inside of the Button class, by replacing "blanks" with "dots"

                           
              
                ###########################
                # Appointment details page
                ###########################
                sleep(2)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div/span[contains(., 'appointment category' )]"))).click()   # Opens the Drop-down menu 
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//mat-option/span[contains(., 'National' )]"))).click()        # Clicks on the option

                sleep(2)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div/span[contains(., 'sub-category' )]"))).click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//mat-option/span[contains(., 'Turkish')]"))).click() 

                sleep(2)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div/span[contains(., 'Application Centre' )]"))).click()
                WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, "//mat-option/span[contains(., 'Poland in Istanbul')]"))).click()          # Any centre that is connected to Istanbul region is fine. I tested through "Reconsideration" category, since I saw availability for all 5 cities. When the "Poland in Istanbul" text is used, it selected the first city that includes this phrase  
                
                # If any centre in Istanbul region is selectable, play the music to warn the user.
                MediaPlayer(r"Music.mp3").play()                 # Short path is better, to be able to run the program on different computers. It does not play without the "r" at the beginning
                sleep(200)                                       # Specify the duration of the play here; otherwise, it will not play
                exit()
            
        except TimeoutException:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "navbarDropdown"))).click()           # Click on "My Account"
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropdown-item"))).click()    # Click on "Dashboard"