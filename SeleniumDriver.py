# AUTHOR: GARRETT BREEDEN
# DESCRIPTION: Automate creating Sales Splits and Sales Clear in JIRA



# TODO: Automatically copy new case created into clipboard (Look into parsing HTML / Screenshotting)
# TODO: https://github.com/kybu/headless-selenium-for-win

from selenium import webdriver
# Allows for keystokes to be passed
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyperclip
import re
import pickle


class SeleniumDriver():
    def __init__(self,):
        self.driver = None
        self.sessionCookies = None

    def loadPage(self, website, title, startSeleniumCheck):
        if startSeleniumCheck == True:
            self.driver = webdriver.Ie()
        self.driver.get(website)
        assert title in self.driver.title  # Ensure jira loaded correctly
        print("Loaded {} successfully".format(title))

    def login(self, username, password):
        

        username_form = self.driver.find_element_by_xpath(
            ".//*[@id='login-form-username']")
        username_form.clear()
        username_form.send_keys(username)

        password_form = self.driver.find_element_by_xpath(
            ".//*[@id='login-form-password']")
        password_form.clear()
        password_form.send_keys(password)

        submit_button = self.driver.find_element_by_xpath(
            ".//*[@id='login-form-submit']")
        submit_button.click()
        

    def createNewTicket(self):
        title = "Dashboard"
        while((title not in self.driver.title) == True):
            sleep(.25)
            print("sleeping .25 seconds to finish loading page")
        
        
        self.loadPage(
            "https://devops.partech.com/jira/secure/Dashboard.jspa", "System Dashboard", False)
        #bbs_element = self.driver.find_element_by_xpath(".//*[@id='brink-bugs-and-support-(bbs)-84']/a")
        
        create_ticket_button = self.driver.find_element_by_xpath('//*[@id="create_link"]')
        create_ticket_button.click()

        title = "Create Issue"
        while((title not in self.driver.title) == True):
            sleep(.25)
            print("sleeping .25 seconds to finish loading page") 

        project_field_element = self.driver.find_element_by_xpath(
            "//*[@id='project-field']")
        project_field_element.clear()
        project_field_element.send_keys("BBS")
        project_field_element.send_keys(Keys.ENTER)

        sleep(.5)
        issue_type_field_element = self.driver.find_element_by_xpath(
            '//*[@id="issuetype-field"]')
        issue_type_field_element.clear()
        issue_type_field_element.send_keys("Task")
        issue_type_field_element.send_keys(Keys.ENTER)
        

        # issue_submit_button = self.driver.find_element_by_xpath(
        #     ".//*[@id='issue-create-submit']")
        # issue_submit_button.click()

    def inputDataToCase(self, summary, clarify, description):
        notifyUsers = '\n\n[~gary_meyer@partech.com] [~garrett_breeden@partech.com] [~steven_eddy@partech.com] [~Derek_puttmann@partech.com] [~angelo_espineli@partech.com] [~chris_wright@partech.com]'
        sleep(1)
        # TODO: Update to use control V and not sendkeys. Much slower on larger cases.
        summary_field = self.driver.find_element_by_xpath(
            '//*[@id="summary"]')
        summary_field.send_keys(summary)

        raw_input_element = self.driver.find_elements_by_partial_link_text('Text')
        raw_input_element[1].click()

        
        description_text_field = self.driver.find_element_by_xpath('//*[@id="description"]')
        description_text_field.click()
        description_text_field.send_keys(clarify, "\n") 
        description_text_field.send_keys(description)
        description_text_field.send_keys(notifyUsers)

        # Set Priority of Case
        severity_drop_down = self.driver.find_element_by_xpath('//*[@id="customfield_10405"]')
        #severity_drop_down.clear()
        
        sleep(.5) #Ensure it properly reloads
        severity_drop_down.click()
        severity_drop_down.send_keys("Minor", Keys.TAB)
        sleep(.5)

        assigned_to_element = self.driver.find_element_by_xpath(
            ".//*[@id='assignee-field']")
        assigned_to_element.clear()
        assigned_to_element.send_keys("Mike Dem")
        sleep(.5)
        assigned_to_element.send_keys(Keys.TAB, Keys.TAB)

        submit_JIRA_case_button = self.driver.find_element_by_xpath('//*[@id="create-issue-submit"]')
        submit_JIRA_case_button.click()

        sleep(.6)
        JIRA_case_number_element = self.driver.find_element_by_xpath('//*[@id="aui-flag-container"]/div/div')
        self.JIRA_case_raw = JIRA_case_number_element.get_attribute("innerHTML")
        self.last_created_JIRA_Case = self.getJIRACase(self.JIRA_case_raw)


    # TODO: Finish Parsing Users Function
    def parseUsers(self, users):
        pass

    # TODO: Enable postAttachment function
    # Let the user control add this until completed
    def postAttachment(self, admin_site, site_id, location_id):
        pass
    
    def getJIRACase(self, searchString):
        regex = re.search(r'(/jira/browse/BBS-\d+)', searchString)
        return regex.groups()[0]
