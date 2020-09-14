from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

# Returns a tuple to indicate status (code, class)
# 1 : Invalid password
# 2 : There's currently no class
# 3 : Presence form not opened yet
# 4 : Presence form filled successfully
# 5 : Presence form already filled
def presence(username, password, success_callback=lambda: None, delay=8, headless=True, logging=None):
    if not logging:
        import logging
        # Setup logging config
        logging.basicConfig(format='[%(asctime)s] - %(message)s', datefmt='%d %b %H:%M:%S', level=logging.INFO)

    # Presence
    try:
        # Opening webdriver
        logging.info('Opening webdriver')
        options = Options()
        if(headless):
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        actions = ActionChains(driver)

        # Main page
        logging.info('Opening main site')
        driver.get('https://akademik.itb.ac.id/')
        driver.find_element_by_id('login').click()

        # Login page
        logging.info('Opening akademik.itb.ac.id login page')
        driver.find_element_by_xpath('//a[@href=\'/login/INA\']').click()

        # INA login page
        logging.info('Login using ITB SSO')
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_xpath('//input[@type=\'submit\']').click()

        # SIX Dashboard
        logging.info('Opening SIX dashboard')
        fullhtml = driver.find_elements_by_tag_name('body')[0].get_attribute('innerHTML')
        try:
            nim = re.search(".*mahasiswa:(.*?)/.*?", fullhtml).group(1)
        except Exception:
            return (1, None)
        class_link = driver.find_elements_by_xpath("//div[contains(@class, 'apps')]//div[contains(@class, 'col-xs-4 col-sm-3 col-md-2 text-center')]")[3]
        class_link.click()

        # SIX Class Menu
        logging.info('Opening SIX class menu')
        current_day_cell = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'bg-info')))
        classes_today = current_day_cell.find_elements_by_xpath('.//div/div[@title]/a')
        classes_schedule = list(map(lambda val: re.sub(r'(..:..-..:..).*', r'\1', val.text).split('-'), classes_today))
        classes_code = list(map(lambda val: val.text[12:18], classes_today))

        # Get current server time (GMT +7)
        t = time.gmtime(time.time() + 25200)
        current_time = time.strftime("%H:%M", t)
        logging.info('Current server time: {}'.format(current_time))

        # Input presence current z`attended class
        for index, schedule in enumerate(classes_schedule):
            # Get schedule time
            start_time, end_time = schedule[0], schedule[1]

            if(start_time <= current_time <= end_time):
                logging.info('Checking {}'.format(classes_code[index]))
                classes_today[index].send_keys(Keys.ENTER)

                # Wait until finished loading
                WebDriverWait(driver, delay).until(EC.invisibility_of_element((By.XPATH, "//*[contains(@class, 'loading')]")))

                # Checking for unpresence button
                try:
                    unpresence_button = driver.find_element_by_id('form_tidakhadir')
                    logging.info('Presence form is filled for {}'.format(classes_code[index]))
                    return (5, classes_code[index])
                except Exception:
                    pass

                # Checking for presence button
                try:
                    presence_button = driver.find_element_by_id('form_hadir')
                    presence_button.click()
                    logging.info('Presence successful')
                    success_callback()
                    return (4, classes_code[index])
                except Exception:
                    logging.info('Presence form currently closed for {}'.format(classes_code[index]))
                    return(3, classes_code[index])

            else:
                logging.info('Currently is not the time for {}'.format(classes_code[index]))

        return (2, None)

    except Exception as exc:
        logging.exception(exc)
    finally:
        time.sleep(5)
        driver.close()
