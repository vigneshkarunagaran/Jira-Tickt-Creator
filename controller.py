from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from retrying import retry
import time
import json

DB = {}
firefox = r"\webdriver\geckodriver.exe"

def loadSettingDB():
    global DB
    with open(r'settings.json', 'r') as fo:
        DB = json.load(fo)


loadSettingDB()


jiraLogin = DB["jiraLogin"]
jiraCreate = DB["jiraCreate"]


# ID's
projectField = 'project-field' 
taskType = 'issuetype-field' 
pageOneNext = 'issue-create-submit'

taskTitle = 'summary'
taskPriority = 'priority-field'
leadingTeam = 'customfield_16126-field' 
contributingTeam = 'customfield_10609-textarea'
lables = 'labels-textarea'
storyPoints = 'customfield_10106'
sprint = 'customfield_10104-field'
assignee = 'assignee-field'
pageTwoCreate = 'issue-create-submit'

subDescription = 'description'
subAcceptance = 'customfield_10903'
pageThreeCreate = 'subtask-create-details-submit'

# IFRAMES
descriptionID = 'mce_0_ifr'
acceptanceCriteriaID = 'mce_6_ifr'

# XPATHS
# browser = webdriver.Chrome(executable_path=chromeDriver)
browser = webdriver.Firefox(executable_path=firefox)

# def openPage(page):
#     pass


# def proceedClick(bt):
#     pass


# def sendKeysToListField(field, byType, text):
#     pass


# def sendKeysToTextField(field, byType, text):
#     pass


# def sendKeysToMCE(field, text):
#     pass

@retry(stop_max_attempt_number=10, wait_exponential_multiplier=500, wait_exponential_max=4000)
def openPage(page):
    browser.get(page)


@retry(stop_max_attempt_number=10, wait_exponential_multiplier=500, wait_exponential_max=4000)
def proceedClick(bt):
    targetField = browser.find_element_by_id(bt)
    targetField.click()


@retry(stop_max_attempt_number=10, wait_exponential_multiplier=500, wait_exponential_max=4000)
def sendKeysToListField(field, byType, text):
    if byType == 'id':
        targetField = browser.find_element_by_id(field)
        targetField.send_keys(Keys.CONTROL + "a")
        targetField.send_keys(text)
        time.sleep(2)
        targetField.send_keys(Keys.RETURN)


@retry(stop_max_attempt_number=10, wait_exponential_multiplier=500, wait_exponential_max=4000)
def sendKeysToTextField(field, byType, text):
    if byType == 'id':
        targetField = browser.find_element_by_id(field)
        targetField.send_keys(text)


@retry(stop_max_attempt_number=10, wait_exponential_multiplier=500, wait_exponential_max=4000)
def sendKeysToMCE(field, text):
    mce_frame = browser.find_element_by_id(field)
    browser.switch_to.frame(mce_frame)
    mce_edit = browser.find_element_by_xpath('//*[@id="tinymce"]')
    mce_edit.send_keys(text)
    browser.switch_to.default_content()


def loginPage():
    openPage(jiraLogin)


def createNewTicket():
    openPage(jiraCreate)


def setProject():
    sendKeysToListField(projectField, 'id', DB["projectText"])
    sendKeysToListField(taskType, 'id', DB["storyText"])
    time.sleep(1)
    proceedClick(pageOneNext)


def setTaskName(taskName):
    sendKeysToTextField(taskTitle, 'id', taskName)


def setTaskPriority():
    sendKeysToListField(taskPriority, 'id', DB["priorityText"])


def setTeams():
    sendKeysToListField(leadingTeam, 'id', DB["teamText"])
    # sendKeysToListField(contributingTeam, 'id', DB["teamText"])


def setDescription(des):
    sendKeysToMCE(descriptionID, des)


def setLables():
    sendKeysToListField(lables, 'id', DB["lableText"])


def setAssignee(mailID):
    sendKeysToListField(assignee, 'id', mailID)


def setStoryPoints(mainTaskPoints):
    sendKeysToTextField(storyPoints, 'id', str(mainTaskPoints))


def setSprint(taskSprint):
    sendKeysToListField(sprint, 'id', taskSprint)


def setAcceptanceCriteria(AcceptanceCriteria):
    sendKeysToMCE(acceptanceCriteriaID, AcceptanceCriteria)


def createTask():
    proceedClick(pageTwoCreate)
    print(browser.current_url)


def createSubTask():
    proceedClick(pageThreeCreate)
    print(browser.current_url)


def redirectSubTaskCreate(redirectURL):
    openPage(redirectURL)


def subTaskDescription(des):
    sendKeysToTextField(subDescription, 'id', des)


def subTaskAcceptance(ac):
    sendKeysToTextField(subAcceptance, 'id', ac)
