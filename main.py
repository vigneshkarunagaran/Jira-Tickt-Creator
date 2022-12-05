from multiprocessing.sharedctypes import Value
from tkinter.scrolledtext import ScrolledText
from turtle import width
import controller as EXE
from tkinter import *
from tkinter import ttk
from datetime import datetime
from time import strftime
import json

DB = {}
def loadSettingDB():
    global DB
    with open(r'settings.json','r') as fo:
        DB = json.load(fo)
    
        
loadSettingDB()

mainTaskAssignList = []
subTaskIDList = []
subTaskAssignList = []
createdMainTask = False
canCreate = False
mainURL = ''

root = Tk()

root.title("Jira Ticket Creator")
# root.resizable(False, False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{}x{}+{}+{}".format(int(screen_width/2),
              580, int(screen_width/2), 0))

tab_parent = ttk.Notebook(root)
mainTab = ttk.Frame(tab_parent)
settingsTab = ttk.Frame(tab_parent)
tab_parent.add(mainTab, text="Workspace")
tab_parent.add(settingsTab, text="Settings")
tab_parent.pack(expand=1, fill='both')

headFrame = ttk.Frame(mainTab, padding=5)
headFrame.grid()
detailFrame = ttk.Frame(mainTab, padding=5)
detailFrame.grid()
assigneFrame = ttk.Frame(mainTab, padding=5)
assigneFrame.grid()
messageFrame = ttk.Frame(mainTab, padding=5)
messageFrame.grid()
controlFrame = ttk.Frame(mainTab, padding=5)
controlFrame.grid()
defaultValueFrame = ttk.Frame(settingsTab, padding=5)
defaultValueFrame.grid(sticky='WE')
membersFrame = ttk.Frame(settingsTab, padding=5)
membersFrame.grid()


def setMessage(log, messType='MESS'):
    current_time = datetime.now().strftime("%H_%M_%S")
    message = '['+current_time + ']' + log + '\n'
    messageBox.tag_config('ERROR', foreground='red')
    messageBox.tag_config('COMP', foreground='green')
    messageBox.tag_config('CREAT', foreground='orange')
    messageBox.tag_config('LOG', foreground='blue')
    messageBox.tag_config('MESS', foreground='black')
    messageBox.insert(END, message, messType)
    messageBox.yview(END)


def loginPage():
    setMessage("Proceeding with logIn", 'LOG')
    EXE.loginPage()


def newTicket():
    setMessage("Proceeding with New Ticket creation ...", 'LOG')
    global mainTaskAssignList
    global subTaskAssignList
    global subTaskIDList
    global createdMainTask
    global mainURL
    global canCreate
    canCreate = False
    mainTaskAssignList = []
    subTaskIDList = []
    subTaskAssignList = []
    createdMainTask = False
    mainURL = ''
    teTaskName.delete(0, END)
    teAC.delete(0, END)
    teAC.insert(0, "Same as Task Name")
    teSub.delete(0, END)
    teSub.insert(0, "Only if Sub-task present")
    teStory.delete(0, END)
    teStory.insert(0, "1")
    EXE.createNewTicket()
    setProject()



def setProject():
    setMessage('Project : Apricot (APRICOT)')
    setMessage('Issue Type : Story')
    EXE.setProject()


def redirectSubTaskCreate():
    if teSub.get() == "Only if Sub-task present":
        setMessage("No Valid URL", 'ERROR')
    else:
        redirectURL = teSub.get()
        EXE.redirectSubTaskCreate(redirectURL)
        setMessage("Redirected to Sub-Task creation", 'LOG')


def createTask():
    global createdMainTask
    global canCreate

    if canCreate:
        if not createdMainTask:
            EXE.createTask()
        else:
            EXE.createSubTask()

        if not createdMainTask and len(subTaskAssignList) != 0:
            createdMainTask = True
            setMessage("Main-Task created, Add Sub-Task and proceed", 'CREAT')
        elif createdMainTask and len(subTaskAssignList) != 0:
            setMessage("Sub-Task created, Add Sub-Task and proceed", 'CREAT')
        elif not createdMainTask and len(subTaskAssignList) == 0:
            createdMainTask = True
            setMessage("    Main-Task creation and completed    ", 'COMP')
            setMessage("========================================")
            newTicket()
        elif createdMainTask and len(subTaskAssignList) == 0:
            setMessage("        Task creation completed         ", 'COMP')
            setMessage("========================================")
            newTicket()
        canCreate = False
    else:
        setMessage("Fill Details with no Errors and Proceed", 'ERROR')
        
            


def setAcceptanceCriteria():
    AcceptanceCriteria = teAC.get()
    if AcceptanceCriteria == 'Same as Task Name':
        AcceptanceCriteria = teTaskName.get()
    setMessage('Acceptance Criteria : "'+AcceptanceCriteria+'"')
    if createdMainTask:
        EXE.subTaskAcceptance(AcceptanceCriteria)
    else:
        EXE.setAcceptanceCriteria(AcceptanceCriteria)
    setTaskName()


def setSprint():
    sprint = teSprint.get()
    if sprint == 'Sprint':
        setMessage("Sprint Details Missing", 'ERROR')
    else:
        setMessage("Sprint : "+sprint)
        EXE.setSprint(sprint)
        setAcceptanceCriteria()


def calculateMainTaskPoints():
    storyPoints = teStory.get()
    if ',' in storyPoints:
        storyPoints =  [int(i) for i in storyPoints.split(',')]
        storyPoints = sum(storyPoints)
    else:
        storyPoints = int(storyPoints)
    if storyPoints in [0, 1, 2, 3]:
        return storyPoints
    elif storyPoints in [4, 5, 6]:
        return 5
    elif storyPoints in [7, 8, 9, 10]:
        return 8
    elif storyPoints in [11, 12, 13, 14, 15, 16]:
        return 13
    elif storyPoints >= 17:
        return 20


def setStoryPoints():
    mainTaskPoints = calculateMainTaskPoints()
    if not createdMainTask:
        assigID = mainTaskAssignList[0]
        setMessage("Main-Task Assignee : "+assigID)
        setMessage("Points : " + str(mainTaskPoints))
        EXE.setAssignee(assigID)
        EXE.setStoryPoints(mainTaskPoints)
        setSprint()

    elif len(subTaskAssignList) > 0:
        assigID = subTaskAssignList.pop()
        setMessage("Sub-Task Assignee : "+assigID)
        EXE.setAssignee(assigID)
        setAcceptanceCriteria()

def setLables():
    setMessage("Lables : OMS-Testing")
    EXE.setLables()
    setStoryPoints()


def setDescription():
    # description = teDes.get()
    # if description == 'Same as Task Name':
    #     description = teTaskName.get()
    # setMessage('Description : "'+description+'"')
    # if createdMainTask:
    #     EXE.subTaskDescription(description)
    # else:
    #     EXE.setDescription(description)
    setLables()


def setTeams():
    setMessage("Leading Team : OMS")
    # setMessage("Contributing Team : OMS", True)
    EXE.setTeams()
    setDescription()


def setTaskPriority():
    setMessage("########################################")
    setMessage("#             Task Details             #")
    setMessage("########################################")
    setMessage("Priority : Medium")
    EXE.setTaskPriority()
    setTeams()


def setTaskName():
    global canCreate
    tName = teTaskName.get()

    if tName == "":
        setMessage("Task Name missing", 'ERROR')
    else:
        taskName = 'Testing : ' + tName
        EXE.setTaskName(taskName)
        setMessage('Task Name : "' + taskName + '"')

        if not createdMainTask:
            setMessage('Proceed for Main-Task creation', 'LOG')
        else:
            setMessage('Proceed for Sub-Task creation', 'LOG')
        canCreate = True


def fillDetails():
    if not createdMainTask:
        setTaskPriority()
    else:
        setTeams()
        
def assigneMain():
    if memberSelected.get() != '':
        mail = DB["teamMembers"][memberSelected.get()]
        
        if len(mainTaskAssignList) == 1:
            mainTaskAssignList.pop()
        mainTaskAssignList.append(mail)
        setMessage('Main Task : ' + memberSelected.get())
    else:
        setMessage('Select a member', 'ERROR')
        
    
def addSub():
    if memberSelected.get() != '':
        mail = DB["teamMembers"][memberSelected.get()]  
        if mail not in subTaskAssignList:
            subTaskIDList.append(memberSelected.get())
            subTaskAssignList.append(mail)
        setMessage('Sub Task : ' + str(subTaskIDList))
    else:
        setMessage('Select a member', 'ERROR')
    

def removeSub():
    if memberSelected.get() != '':
        mail = DB["teamMembers"][memberSelected.get()]
        if mail not in subTaskAssignList:
            pass
        else:
            subTaskIDList.remove(memberSelected.get())
            subTaskAssignList.remove(mail)   
        setMessage('Sub Task : ' + str(subTaskIDList))
    else:
        setMessage('Select a member', 'ERROR')
    

Label(detailFrame, text="Task Name").grid(column=0, row=0, sticky='w')
teTaskName = Entry(detailFrame, width=90)
teTaskName.grid(column=1, row=0, sticky='w')

Label(detailFrame, text="Sprint").grid(column=0, row=1, sticky='w')
teSprint = Entry(detailFrame, width=90)
teSprint.grid(column=1, row=1, sticky='w')
teSprint.insert(0, "Sprint")

Label(detailFrame, text="Acceptance").grid(column=0, row=2, sticky='w')
teAC = Entry(detailFrame, width=90)
teAC.grid(column=1, row=2, sticky='w')
teAC.insert(0, "Same as Task Name")

Label(detailFrame, text="Story Point").grid(column=0, row=3, sticky='w')
teStory = Entry(detailFrame, width=90)
teStory.grid(column=1, row=3, sticky='w')
teStory.insert(0, "1")

Label(detailFrame, text="Members").grid(column=0, row=4, sticky='w')
memberSelected = StringVar()
teMembers = OptionMenu(detailFrame, memberSelected, *DB["teamMembers"].keys())
teMembers.grid(column=1, row=4, sticky='WE')

taskFrame = ttk.Frame(detailFrame, padding=5)
taskFrame.grid(column=1, row=5, sticky='WE')

Button(taskFrame, text="Add Main",
       command=assigneMain).grid(column=0, row=0, sticky='WE')
Button(taskFrame, text="Add Sub",
       command=addSub).grid(column=1, row=0, sticky='WE')
# Button(taskFrame, text="Remove Main",
#        command=removeMain).grid(column=2, row=0, sticky='WE')
Button(taskFrame, text="Remove Sub",
       command=removeSub).grid(column=3, row=0, sticky='WE')

Button(detailFrame, text="Sub Task URL",
       command=redirectSubTaskCreate).grid(column=0, row=6, sticky='w')

teSub = Entry(detailFrame, width=90)
teSub.grid(column=1, row=6, sticky='w')
teSub.insert(0, "Only if Sub-task present")

messageBox = ScrolledText(messageFrame, height=15, width=70)
messageBox.grid(column=0, row=0)

Button(controlFrame, text="LogIn", width=20,
       command=loginPage).grid(column=0, row=1)
Button(controlFrame, text="New Ticket", width=20,
       command=newTicket).grid(column=1, row=1)
Button(controlFrame, text="Fill Details", width=20,
       command=fillDetails).grid(column=2, row=1)
Button(controlFrame, text="Create", width=20,
       command=createTask).grid(column=3, row=1)
# Button(controlFrame, text="Test", width=20,
#        command=changeClour).grid(column=4, row=1)

###########################################
#                 SETTINGS
###########################################

def insertMembers(memb):
    text = json.dumps(memb, indent=0)
    memberBox.insert(END, text)

# def updateSetting():
#     DB["projectText"] = projectText.get()
#     DB["storyText"] = storyText.get()
#     DB["priorityText"] = priorityText.get()
#     DB["teamText"] = teamText.get()
#     DB["lableText"] = lableText.get()
#     DB["teamMembers"] = json.loads(memberBox.get("1.0", END))
    
#     EXE.updateSetting(DB)
#     loadSettingDB()
    # teMembers.add_command (Value : *DB["teamMembers"].keys()))
    # memberSelected.set('')
    # teMembers['menu'].delete(0, END)
    # new_choices = DB["teamMembers"].keys()
    # for choice in new_choices:
    #     teMembers['menu'].add_command(label=choice, command=ttk._setit(memberSelected, choice))
    #     teMembers.add_command(label=choice, command=lambda x=choice: show(x))
    


Label(defaultValueFrame, text="Project Name").grid(column=0, row=0, sticky='w')
projectText = Entry(defaultValueFrame, width=50)
projectText.grid(column=1, row=0, sticky='w')
projectText.insert(0, DB["projectText"])

Label(defaultValueFrame, text="Task Type").grid(column=0, row=1, sticky='w')
storyText = Entry(defaultValueFrame, width=50)
storyText.grid(column=1, row=1, sticky='w')
storyText.insert(0, DB["storyText"])

Label(defaultValueFrame, text="Priority").grid(column=0, row=2, sticky='w')
priorityText = Entry(defaultValueFrame, width=50)
priorityText.grid(column=1, row=2, sticky='w')
priorityText.insert(0, DB["priorityText"])

Label(defaultValueFrame, text="Team").grid(column=0, row=3, sticky='w')
teamText = Entry(defaultValueFrame, width=50)
teamText.grid(column=1, row=3, sticky='w')
teamText.insert(0, DB["teamText"])

Label(defaultValueFrame, text="Task Lable").grid(column=0, row=4, sticky='w')
lableText = Entry(defaultValueFrame, width=50)
lableText.grid(column=1, row=4, sticky='w')
lableText.insert(0, DB["lableText"])

memberBox = ScrolledText(membersFrame, height=15, width=70)
memberBox.grid(column=0, row=0)
insertMembers(DB["teamMembers"])

# Button(membersFrame, text="Update", width=20,
#        command=updateSetting).grid(column=0, row=1, sticky='WE')

root.mainloop()
