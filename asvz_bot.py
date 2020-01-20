#!/home/<user>/asvz_bot_python/bin/python

"""
Created on: Mar 20, 2019
Author: Julian Stiefel
License: BSD 3-Clause
Description: Script for automatic enrollment in ASVZ classes
"""

############################# Edit this: ######################################

#ETH credentials:
username = 'xxxx'
password = 'xxxx'
day = 'Donnerstag'
facility = 'Sport Center Polyterrasse'
lesson_time = '19:30'
enrollment_time_difference = 22 #how many hours before registration starts
#link to particular sport on ASVZ Sportfahrplan, e.g. cycling class:
sportfahrplan_particular = 'https://asvz.ch/426-sportfahrplan?f[0]=sport:45645'

###############################################################################

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def waiting_fct():
    #if script is started before registration time. Does only work if script is executed on day before event.
    currentTime = datetime.today()
    enrollmentTime = datetime.strptime(lesson_time, '%H:%M')
    enrollmentTime = enrollmentTime.replace(hour=enrollmentTime.hour + (24-enrollment_time_difference))
    
    while currentTime.hour < enrollmentTime.hour:
        print("Wait for enrollment to open")
        time.sleep(60)
        currentTime = datetime.today()

    if currentTime.hour == enrollmentTime.hour:
        while currentTime.minute < enrollmentTime.minute:
            print("Wait for enrollment to open")
            time.sleep(30)
            currentTime = datetime.today()
	
    return
    
    
def asvz_enroll():
    options = Options()
    options.headless = True
    options.add_argument("--private") #open in private mode to avoid different login scenario
    driver = webdriver.Firefox(options = options)
    
    try:
        driver.get(sportfahrplan_particular)
        driver.implicitly_wait(20) #wait 20 seconds if not defined differently
        print("Headless Firefox Initialized")
        #find corresponding day div:
        day_ele = driver.find_element_by_xpath("//div[@class='teaser-list-calendar__day'][contains(., '" + day + "')]")
        #search in day div after corresponding location and time
        day_ele.find_element_by_xpath(".//li[@class='btn-hover-parent'][contains(., '" + facility + "')][contains(., '" + lesson_time + "')]").click()

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn--block btn--icon relative btn--primary-border' or @class='btn btn--block btn--icon relative btn--primary']"))).click()

        #switch to new window:
        time.sleep(2) #necessary because tab needs to be open to get window handles
        tabs = driver.window_handles
        driver.switch_to.window(tabs[1])
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-default ng-star-inserted' and @title='Login']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-warning btn-block' and @title='SwitchAai Account Login']"))).click()

        #choose organization:
        organization = driver.find_element_by_xpath("//input[@id='userIdPSelection_iddtext']")
        organization.send_keys('ETH Zurich')
        organization.send_keys(u'\ue006')

        driver.find_element_by_xpath("//input[@id='username']").send_keys(username)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        #wait for button to be clickable for 5 minutes, which is more than enough
        #still needs to be tested what happens if we are on the page before button is enabled
        WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='btnRegister' and @class='btn-primary btn enrollmentPlacePadding ng-star-inserted']"))).click()
        print("Successfully enrolled. Train hard and have fun!")
    except: #using non-specific exceptions, since there are different exceptions possible: timeout, element not found because not loaded, etc. 
        driver.quit()
        raise #re-raise previous exception

    driver.quit #close all tabs and window
    return True

#run enrollment script:
i = 0 #count
success = False

waiting_fct()

#if there is an exception (no registration possible), enrollment is tried again in total 5 times and then stopped to avoid a lock-out
while not success:
    try:
        success = asvz_enroll()
        print("Script successfully finished")
    except:
        if i<4:
            i += 1
            print("Enrollment failed. Start try number {}".format(i+1))
            pass
        else:
            raise
        
