from flask import Flask, render_template, redirect, request, session
import json
import base64, os
import time
import pyrebase
import symptomClassifierAPI
import re
import calendar
from googlesearch import search
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document, \
    RecipientViewRequest

app = Flask(__name__)   

#docusign config
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjY4MTg1ZmYxLTRlNTEtNGNlOS1hZjFjLTY4OTgxMjIwMzMxNyJ9.eyJUb2tlblR5cGUiOjUsIklzc3VlSW5zdGFudCI6MTU5ODkwMzc3MSwiZXhwIjoxNTk4OTMyNTcxLCJVc2VySWQiOiJkNzJjODkwYi0zZGFjLTQ3NjMtOTVmMS0yYzM1OWQ3NWFkZTkiLCJzaXRlaWQiOjEsInNjcCI6WyJzaWduYXR1cmUiLCJjbGljay5tYW5hZ2UiLCJvcmdhbml6YXRpb25fcmVhZCIsInJvb21fZm9ybXMiLCJncm91cF9yZWFkIiwicGVybWlzc2lvbl9yZWFkIiwidXNlcl9yZWFkIiwidXNlcl93cml0ZSIsImFjY291bnRfcmVhZCIsImRvbWFpbl9yZWFkIiwiaWRlbnRpdHlfcHJvdmlkZXJfcmVhZCIsImR0ci5yb29tcy5yZWFkIiwiZHRyLnJvb21zLndyaXRlIiwiZHRyLmRvY3VtZW50cy5yZWFkIiwiZHRyLmRvY3VtZW50cy53cml0ZSIsImR0ci5wcm9maWxlLnJlYWQiLCJkdHIucHJvZmlsZS53cml0ZSIsImR0ci5jb21wYW55LnJlYWQiLCJkdHIuY29tcGFueS53cml0ZSJdLCJhdWQiOiJmMGYyN2YwZS04NTdkLTRhNzEtYTRkYS0zMmNlY2FlM2E5NzgiLCJhenAiOiJmMGYyN2YwZS04NTdkLTRhNzEtYTRkYS0zMmNlY2FlM2E5NzgiLCJpc3MiOiJodHRwczovL2FjY291bnQtZC5kb2N1c2lnbi5jb20vIiwic3ViIjoiZDcyYzg5MGItM2RhYy00NzYzLTk1ZjEtMmMzNTlkNzVhZGU5IiwiYW1yIjpbImludGVyYWN0aXZlIl0sImF1dGhfdGltZSI6MTU5ODkwMzc2OCwicHdpZCI6IjIwZWFkZDIyLTVjN2QtNGFjNi04MDEyLWFhNjlkMjAzMjNkOSJ9.UiLPgNb-O7FVJaYix0BcJgqMe9qVWIDh0a3QAVgsEGylYWQeVW99bRjb4guG2-DUwQRA2Fhl8wYoaJBrkxWLX2wQGuSPgUeDS5riRx8NExyvk_V5aEmy23o-Kaz0l4KLqg3RgA_Ep0YriTLjiszJPWY7-b4Bp2QvtJ96-6wgIaOu-ZgmlEho3NmGvi4VsbV2fnB82oaSBxhs0bQ0ZcT8rTmASmu4kFOgSVLLwu43TNHGPcbfgXNl-N-WdvpTvcfwHh2bYmmOKNJNOcVYuMI54DJO_6-7tDCy31YuN2MAC95_PVDLVz0V3SqA4W3Ka5rQjc1RywkUjXnyR04iq16Exw'
account_id = '8999522'
signer_name = 'Roshan Warman'
signer_email = 'roshanwarman22@gmail.com'
confirm_file_upload = 'docuSignExamples/exEHR.pdf'
second_confirm_doctor = "docuSignExamples/docusign.pdf"
base_url = 'http://localhost:5000'
client_user_id = '123'
authentication_method = 'None'
base_path = 'https://demo.docusign.net/restapi'

if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'development'

APP_PATH = os.path.dirname(os.path.abspath(__file__))


def signFirstThingy(file_name_path):
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = Document(
        document_base64=base64_file_content,
        name='File Upload',
        file_extension='pdf',
        document_id=1
    )


    signer = Signer(
        email=signer_email, name=signer_name, recipient_id="1", routing_order="1",
        client_user_id=client_user_id,
    )

    sign_here = SignHere(document_id='1', page_number='1', recipient_id='1', tab_label='Your Name, Doctor Nanme',x_position='195', y_position='147')
    


    

    signer.tabs = Tabs(sign_here_tabs=[sign_here])
    envelope_definition = EnvelopeDefinition(
        email_subject="blahblahblahheheh",
        documents=[document],
        recipients=Recipients(signers=[signer]),
        status="sent"
    )


    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

    envelope_id = results.envelope_id
    recipient_view_request = RecipientViewRequest(
        authentication_method=authentication_method, client_user_id=client_user_id,
        recipient_id='1', return_url=base_url + '/',
        user_name=signer_name, email=signer_email
    )

    results = envelope_api.create_recipient_view(account_id, envelope_id,
                                                 recipient_view_request=recipient_view_request)

    return results.url



app.secret_key = '#d\xe9X\x00\xbe~Uq\xebX\xae\x82\x1fs\t\xb4\x99\xa3\x87\xe6.\xd1_'

#Rajat config
firebaseConfig = {
  "apiKey": "AIzaSyCI_ONhAh6vn9mukkqgW7N7HK73iURIJoI",
  "authDomain": "hackforafrica.firebaseapp.com",
  "databaseURL": "https://hackforafrica.firebaseio.com",
  "projectId": "hackforafrica",
  "storageBucket": "hackforafrica.appspot.com",
  "messagingSenderId": "772320941941",
  "appId": "1:772320941941:web:a1907b15aa8e1b0af3e53c",
  "measurementId": "G-SL800DE53W"
}

#Roshan config
# firebaseConfig = {
#     "apiKey": "AIzaSyAMTa6hwa_LiyBNwerTor1agnn7QYavoAE",
#     "authDomain": "tellusdoc.firebaseapp.com",
#     "databaseURL": "https://tellusdoc.firebaseio.com",
#     "projectId": "tellusdoc",
#     "storageBucket": "tellusdoc.appspot.com",
#     "messagingSenderId": "315068328660",
#     "appId": "1:315068328660:web:24c07ca8e258652ebb2941",
#     "measurementId": "G-E5YDS58WWL"
#   }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()

from firebase import firebase
userDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/userInfo')
doctorInfoDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/doctorInfo')
doctorPortalDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/doctorPortal')
doctorChat = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/doctorChat')
diagnosisTableData = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/diagnosisTableData')
storeUserApptReqDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/storeUserApptReq')
docSchedDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/storeCalendarDataTable')
storeCalendarDatabaseU = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/storeCalendarDataTableUser')
storeAptDateFinal = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/storeAptDateFinal')

def idGivenEmail(email):
    listVersionOfEmail = list(email) 
    for i in range(0, len(listVersionOfEmail)):
        if listVersionOfEmail[i] == '.':
            listVersionOfEmail[i] = '1'
        elif listVersionOfEmail[i] == '*':
            listVersionOfEmail[i] = '2'
    email = "".join(listVersionOfEmail)
    return email

@app.route("/")                   
def home():
    if 'user' in session:
        if session['AccountType'] == 'User':
            nameVar = userDatabase.get('/userInfo', idGivenEmail(session['user']))['Names']
            day = storeAptDateFinal.get('/storeAptDateFinal', idGivenEmail(session['user']))
            if day != None:
                return render_template('userLanding.html', signInStatus = "Sign Out", acctType=session['AccountType'], dayVar=day['day'], timeVar=day['time'], monthVar=day['month'], nameVar=nameVar)
            else:
                return render_template('userLanding.html', signInStatus = "Sign Out", acctType=session['AccountType'], dayVar="",nameVar=nameVar)
        else:
            nameVar = doctorInfoDatabase.get('/doctorInfo', idGivenEmail(session['user']))['Names']
            day = storeAptDateFinal.get('/storeAptDateFinal', 'lisa1bart@gmail1com')
            if day != None:
                return render_template('doctorLand2.html', signInStatus = "Sign Out", acctType=session['AccountType'], nameVar=nameVar, dayVar=day['day'], timeVar=day['time'], monthVar=day['month'], userNameVar=day['name'])         
            else:
                return render_template('doctorLand2.html', signInStatus = "Sign Out", acctType=session['AccountType'], nameVar=nameVar, dayVar="empty")
             
    else: 
        return render_template('land.html') 

@app.route("/sendDoctorFile", methods=['POST'])                   
def sendDoctorFile():  
    if request.method == "POST":
        return redirect(signFirstThingy(confirm_file_upload))
    return redirect('/')    


@app.route('/landFR')
def landFR():
    return render_template("landFR.html")

@app.route('/landSW')
def landSW():
    return render_template("landSW.html")


@app.route("/diagnose", methods=['GET', 'POST'])                   
def diagnose():               
    if request.method == 'GET':
        if 'user' in session:
            if session['AccountType'] == "User":
                symList = ['Abdominal pain', 'Anxiety', 'Back pain', 'Burning eyes', 'Burning in the throat', 'Cheek swelling', 'Chest pain', 'Chest tightness', 'Chills', 'Cold sweats', 'Cough', 'Dizziness', 'Drooping eyelid', 'Dry eyes', 'Earache', 'Early satiety', 'Eye pain', 'Eye redness', 'Fast, deepened breathing', 'Feeling of foreign body in the eye', 'Fever', 'Going black before the eyes', 'Headache', 'Heartburn', 'Hiccups', 'Hot flushes', 'Increased thirst', 'Itching eyes', 'Itching in the nose', 'Lip swelling', 'Memory gap', 'Menstruation disorder', 'Missed period', 'Nausea', 'Neck pain', 'Nervousness', 'Night cough', 'Pain in the limbs', 'Pain on swallowing', 'Palpitations', 'Paralysis', 'Reduced appetite', 'Runny nose', 'Shortness of breath', 'Skin rash', 'Sleeplessness', 'Sneezing', 'Sore throat', 'Sputum', 'Stomach burning', 'Stuffy nose', 'Sweating', 'Swollen glands in the armpits', 'Swollen glands on the neck', 'Tears', 'Tiredness', 'Tremor at rest', 'Unconsciousness', 'Vomiting', 'Vomiting blood', 'Weight gain', 'Wheezing'] 
                data = doctorPortalDatabase.get('/diagnosisTableData', idGivenEmail(session['user']))
                tasks = []
                if data != None:
                    for i in range(0, len(data['Confidence'])):
                        tasks.append({'Name': data['Name'][i],'Symptoms': ', '.join(data['Symptoms'][i]),'Confidence': data['Confidence'][i], "Spec": ', '.join(data['Spec'][i]) })
                return render_template('diagnose.html', signInStatus = "Sign Out", symList=symList, tasks=tasks, acctType=session['AccountType'])
            else:
                return redirect('/')
        else:
            return redirect('/signUp')
    else:
        data = request.form.keys()
        symptomInput = []
        for sym in data:
            symptomInput.append(sym)
        print(symptomInput)
        
        diagnoses_json, main_diagnosis, warnings = symptomClassifierAPI.symptomClassifierFunc(symptomInput=symptomInput)
        if len(diagnoses_json) > 0:
                data = doctorPortalDatabase.get('/doctorPortal', idGivenEmail(session['user']))
                data['Diagnosis'] = main_diagnosis['Professional Name']
                symptomInputString = ', '.join(symptomInput)
                data['Symptoms'] = symptomInputString           
                
                for url in search(symptomInput[0], tld="com", num=1, stop=1, pause=0):
                    data['SymptomsLink'] = url
                for url in search(data['Diagnosis'], tld="com", num=1, stop=1, pause=0):
                    data['DiagnosisLink'] = url
                db.child("doctorPortal").child(idGivenEmail(session['user'])).set(data) 

                commonNameLst = []
                confidenceLst = []
                specOuterLst = []
                symOuterLst = []
                for possibleDiagnosis in diagnoses_json:
                    symOuterLst.append(symptomInput)
                    issue = possibleDiagnosis['Issue']
                    commonNameLst.append(issue['Name'])
                    confidenceLst.append(issue['Accuracy'])
                    spec = possibleDiagnosis['Specialisation']
                    specLst = []
                    for eachSpec in spec:
                        specLst.append(eachSpec['Name'])
                    specOuterLst.append(specLst)

                db.child("diagnosisTableData").child(idGivenEmail(session['user'])).set({"Name": commonNameLst, "Confidence": confidenceLst, "Symptoms": symOuterLst, "Spec": specOuterLst})

                return redirect('/diagnose')
        else:
            return redirect('/diagnose')

@app.route("/nlp", methods=['POST'])
def nlp():
    paragraph = "dizzy"
    symDict = {'Abdominal pain', 'Anxiety', 'Back pain', 'Burning eyes', 'Burning in the throat', 'Cheek swelling', 'Chest pain', 'Chest tightness', 'Chills', 'Cold sweats', 'Cough', 'Dizziness', 'Drooping eyelid', 'Dry eyes', 'Earache', 'Early satiety', 'Eye pain', 'Eye redness', 'Fast, deepened breathing', 'Feeling of foreign body in the eye', 'Fever', 'Going black before the eyes', 'Headache', 'Heartburn', 'Hiccups', 'Hot flushes', 'Increased thirst', 'Itching eyes', 'Itching in the nose', 'Lip swelling', 'Memory gap', 'Menstruation disorder', 'Missed period', 'Nausea', 'Neck pain', 'Nervousness', 'Night cough', 'Pain in the limbs', 'Pain on swallowing', 'Palpitations', 'Paralysis', 'Reduced appetite', 'Runny nose', 'Shortness of breath', 'Skin rash', 'Sleeplessness', 'Sneezing', 'Sore throat', 'Sputum', 'Stomach burning', 'Stuffy nose', 'Sweating', 'Swollen glands in the armpits', 'Swollen glands on the neck', 'Tears', 'Tiredness', 'Tremor at rest', 'Unconsciousness', 'Vomiting', 'Vomiting blood', 'Weight gain', 'Wheezing'}
    symList = []
    paragraphList = paragraph.split()
    for word in paragraphList:
        if word in symDict:
            symList.append(word)
    if len(symList) >= 1:
        return "yo"
         

@app.route("/scheduleUser", methods = ['POST'])                   
def scheduleUser():
    # description = request.form['Description']
    uSchedData = storeCalendarDatabaseU.get('/storeCalendarDataTableUser', idGivenEmail(session['user']))   
    print("lemon", uSchedData)
    if uSchedData != None:
        uSchedList = uSchedData.keys()
        uSchedDict = set(uSchedList)
        doctorSchedData = docSchedDatabase.get('/storeCalendarDataTable', None)
        for doc in doctorSchedData:
            intersection = uSchedDict.intersection(doctorSchedData[doc].keys())
            if len(intersection) != 0:
                keyVar = list(intersection)
                for k in keyVar:
                    intersection2 = set(uSchedData[k][0]).intersection(doctorSchedData[doc][k][0])
                    if len(intersection2) != 0:
                        finalTime = list(intersection2)[0]
                        currDoctorUserData = doctorPortalDatabase.get('/doctorPortal', idGivenEmail(session['user']))
                        print(currDoctorUserData)
                        if currDoctorUserData != None:
                            currDoctorUserData['Date'] = uSchedData[k][1] + " " + k + " @ "  + finalTime + " EST "
                            currDoctorUserData['Link'] = "2"
                            db.child("doctorPortal").child(idGivenEmail(session['user'])).set(currDoctorUserData)
                            db.child("storeAptDateFinal").child(idGivenEmail(session['user'])).set({"day": k, "time": finalTime[0:5], "month": uSchedData[k][1]})
                            db.child("storeAptDateFinal").child(idGivenEmail('lisa.bart@gmail.com')).set({"day": k, "time": finalTime[0:5], "month": uSchedData[k][1], "name": session['name']})
                        return redirect('/')
        currDoctorUserData = doctorPortalDatabase.get('/doctorPortal', idGivenEmail(session['user']))
        if currDoctorUserData != None:
            currDoctorUserData['Date'] = "Apt Passed"
            db.child("doctorPortal").child(idGivenEmail(session['user'])).set(currDoctorUserData)
        return redirect('/')
    else:
        return redirect('/scheduleU')

@app.route("/scheduleDoctor")                   
def scheduleDoctor():  
    firebaseData = doctorPortalDatabase.get('/storeCalendarDataTable', idGivenEmail(session['user']))
    if firebaseData != None:
        print("bro", firebaseData)
        dataList = []
        for key in firebaseData.keys():
            dataList.append({"Month": firebaseData[key][1], "Date": int(key), "Time": firebaseData[key][0], "Year": firebaseData[key][2]})
        print("yo", dataList)
        return render_template('calendar.html', signInStatus = "Sign Out", data=json.dumps(dataList))
    else:
        return render_template('calendar.html')
        
@app.route('/storeCalendarData', methods = ['POST'])
def storeCalendarData():
    jsdata = request.form['javascript_data']
    jsonLoadData = json.loads(jsdata)
    time = jsonLoadData['time']
    day = jsonLoadData['date']
    month = jsonLoadData['month']
    year = jsonLoadData['year']
    # day = getDay(date)
    fireBaseCalendarData = doctorPortalDatabase.get('/storeCalendarDataTable', idGivenEmail(session['user']))
    if fireBaseCalendarData != None:
        fireBaseCalendarData[day] = [time, month, year]
        db.child("storeCalendarDataTable").child(idGivenEmail(session['user'])).set(fireBaseCalendarData)
    else:
        db.child("storeCalendarDataTable").child(idGivenEmail(session['user'])).set({int(day): [time, month, year]})
    return 'success'
def getDay(timeVar):
    timeArr = str(timeVar).split()
    return timeArr[1][:-1]

@app.route('/deleteCalendarData', methods = ['POST'])
def deleteCalendarData():
    jsdata = request.form['javascript_data']
    jsonLoadData = json.loads(jsdata)
    date = jsonLoadData['date']
    day= getDay(date)
    fireBaseCalendarData = doctorPortalDatabase.get('/storeCalendarDataTable', idGivenEmail(session['user']))
    if fireBaseCalendarData != None:
        fireBaseCalendarData.pop(day)
        db.child("storeCalendarDataTable").child(idGivenEmail(session['user'])).set(fireBaseCalendarData)
    return 'success'

@app.route("/scheduleU")                   
def scheduleU():  
    firebaseData = storeCalendarDatabaseU.get('/storeCalendarDataTableUser', idGivenEmail(session['user']))
    if firebaseData != None:
        dataList = []
        for key in firebaseData.keys():
            dataList.append({"Month": firebaseData[key][1], "Date": int(key), "Time": firebaseData[key][0], "Year": firebaseData[key][2]})
        print(dataList)
        return render_template('calendarUser.html', data=json.dumps(dataList), acctType=session['AccountType'])
    else:
        return render_template('calendarUser.html', acctType=session['AccountType'])
        
@app.route('/storeCalendarDataUser', methods = ['POST'])
def storeCalendarDataUser():
    jsdata = request.form['javascript_data']
    jsonLoadData = json.loads(jsdata)
    time = jsonLoadData['time']
    day = jsonLoadData['date']
    month = jsonLoadData['month']
    year = jsonLoadData['year']
    # day = getDay(date)
    fireBaseCalendarData = doctorPortalDatabase.get('/storeCalendarDataTableUser', idGivenEmail(session['user']))
    if fireBaseCalendarData != None:
        fireBaseCalendarData[day] = [time, month, year]
        db.child("storeCalendarDataTableUser").child(idGivenEmail(session['user'])).set(fireBaseCalendarData)
    else:
        db.child("storeCalendarDataTableUser").child(idGivenEmail(session['user'])).set({int(day): [time, month, year]})
    return 'success'
def getDay(timeVar):
    timeArr = str(timeVar).split()
    print(timeArr)
    return timeArr[1][:-1]

@app.route('/deleteCalendarDataUser', methods = ['POST'])
def deleteCalendarDataUser():
    jsdata = request.form['javascript_data']
    jsonLoadData = json.loads(jsdata)
    date = jsonLoadData['date']
    day= getDay(date)
    fireBaseCalendarData = doctorPortalDatabase.get('/storeCalendarDataTableUser', idGivenEmail(session['user']))
    if fireBaseCalendarData != None:
        fireBaseCalendarData.pop(day)
        db.child("storeCalendarDataTableUser").child(idGivenEmail(session['user'])).set(fireBaseCalendarData)
    return 'success'


#for putting filler data into table
@app.route("/testRoute")                   
def dummyData():  
    data = doctorChat.get('/doctorChat', None)
    return data

@app.route("/chat")                   
def chat():  
    if 'name' in session:
        msgDict = doctorPortalDatabase.get('/doctorChat', idGivenEmail(session['name']))
        msgList = []
        if msgDict != None:
            for i in range(0, len(msgDict["Chat"])):                
                timeList = re.split("[, ]", msgDict["Time"][i])
                if len(timeList) > 6:
                    timeList.remove(timeList[0])
                formattedTime = timeList[0] + ' on ' + str(list(calendar.month_abbr).index(timeList[2])) + '/' + timeList[3] + '/' + timeList[5][:-2]
                msgList.append({"Chat": msgDict["Chat"][i], "Time": formattedTime, "Type": msgDict["Type"][i]})
        return render_template('chat.html', msgDict=msgList, acctType=session['AccountType'], currUser=session['name'])
    else:
        return redirect('/signUp')

@app.route("/chatDoctor")                   
def chatDoctorGeneric():
    doctorChatDict = doctorPortalDatabase.get('/doctorChat', None)
    info = []
    for i,person in enumerate(doctorChatDict):
        lastChat = doctorChatDict[person]['Chat'][-1]
        info.append( {"Name": person, "Question": lastChat})
    if len(info) >= 1:
        chattingWith = "Rajat Doshi" #info[0]["Name"]
        msgDict = doctorPortalDatabase.get('/doctorChat', chattingWith)
        msgList = []
        if msgDict != None:
            for i in range(0, len(msgDict["Chat"])):
                msgList.append({"Chat": msgDict["Chat"][i], "Time": msgDict["Time"][i], "Type": msgDict["Type"][i]})
        return render_template('chatDoctor.html', signInStatus = 'Sign Out' , tasks=info, msgDict=msgList, chattingWith=chattingWith, )
    else:
        return render_template('chatDoctor.html', signInStatus = 'Sign Out', acctType=session['AccountType'])       

@app.route("/chatDoctor/<chattingWith>")                   
def chatDoctor(chattingWith): 
    msgDict = doctorPortalDatabase.get('/doctorChat', chattingWith)
    msgList = []
    if msgDict != None:
        for i in range(0, len(msgDict["Chat"])):
            msgList.append({"Chat": msgDict["Chat"][i], "Time": msgDict["Time"][i], "Type": msgDict["Type"][i]}) 
    return render_template('chatDoctor.html', signInStatus = 'Sign Out' , msgDict=msgList, chattingWith=chattingWith)

@app.route("/sendMessageDoctor/<chattingWith>", methods=['POST'])
def sendMessageDoctor(chattingWith):
    chatMsg = request.form['chatMsg']
    data = doctorPortalDatabase.get('/doctorChat', chattingWith)
    print(data)
    if data != None:
        data['Chat'].append(chatMsg)
        data['Time'].append(time.strftime('%l:%M%p on %b %d, %Y'))
        data['Type'].append("doctor")
    else:
        data = {"Chat": [chatMsg], "Time": [time.strftime('%l:%M%p on %b %d, %Y')], "Type": ["doctor"]}
    
    db.child("doctorChat").child(chattingWith).set(data)    
    return redirect('/chatDoctor/'+chattingWith)

@app.route("/sendMessageUser", methods=['POST'])
def sendMessageUser():
    chatMsg = request.form['chatMsg']
    data = doctorPortalDatabase.get('/doctorChat', idGivenEmail(session['name']))
    print(data)
    if data != None:
        data['Chat'].append(chatMsg)
        data['Time'].append(time.strftime('%l:%M%p on %b %d, %Y'))
        data['Type'].append("user")
    else:
        data = {"Chat": [chatMsg], "Time": [time.strftime('%l:%M%p on %b %d, %Y')], "Type": ["user"]}
    
    db.child("doctorChat").child(idGivenEmail(session['name'])).set(data)   
    return redirect('/chat')

@app.route("/doctorPortal")                   
def doctorsPortal():  
    doctorPortalList = getPortalInfo()
    return render_template('doctorsPortal.html', signInStatus = 'Sign Out', tasks=doctorPortalList)
def getPortalInfo():
    portalDict = doctorPortalDatabase.get('/doctorPortal', None)
    portalList = []
    if portalDict != None:
        portalList = [value for value in portalDict.values()]
    return portalList

@app.route("/signIn", methods=['GET', 'POST'])
def signIn():
    if request.method == 'GET':
        return redirect('/')
    else: 
        #get email and password from html form
        email = request.form['email']
        password = request.form['psw']
        
        #try loggin using oAuth from firebase
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except:
            return render_template('land.html')
        session['user'] = auth.get_account_info(user['idToken'])['users'][0]['email']
        try:
            session['name'] = userDatabase.get('/userInfo', idGivenEmail(session['user']))['Names']
            session['AccountType'] = userDatabase.get('/userInfo', idGivenEmail(session['user']))['AccountType']
        except:
            session['name'] = userDatabase.get('/doctorInfo', idGivenEmail(session['user']))['Names']
            session['AccountType'] = userDatabase.get('/doctorInfo', idGivenEmail(session['user']))['AccountType']
        return redirect('/')            

@app.route("/signUp2/<email>", methods=['GET', 'POST'])                   
def signUp2(email):
    if request.method == 'GET':
        return render_template('createAccount2.html', email=email)
    else:
        data = userDatabase.get('/doctorInfo', idGivenEmail(email))
        data['medicallicense'] = request.form['medicallicense']
        data['employeer'] = request.form['employeer']
        data['medSchoolName'] = request.form['medSchoolName']
        data['years'] = request.form['years']
        db.child("doctorInfo").child(idGivenEmail(email)).set(data)
        
        session['user'] = email
        otherMetaData = userDatabase.get('/doctorInfo', idGivenEmail(email))
        session['name'] = otherMetaData['Names']
        session['AccountType'] = otherMetaData['AccountType']
        return  redirect(signFirstThingy(second_confirm_doctor))



@app.route("/signUp", methods=['GET', 'POST'])                   
def signUp():
    if request.method == 'GET':
        return render_template('createAccount.html', errorMessage="")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['psw']
        passwordRepeat = request.form['psw-repeat']
        acctType = request.form['acctType']

        if password != passwordRepeat:
            return render_template('createAccount.html', errorMessage="Passwords Do Not Match")
        try:
            user = auth.create_user_with_email_and_password(email, password)
        except Exception as e:
            fullErrorMessage = e.args[1]
            err = json.loads(fullErrorMessage)["error"]["message"]
            return render_template('createAccount.html', errorMessage=err)

        if acctType == 'User':
            db.child("userInfo").child(idGivenEmail(email)).set({"Names": name, "Email": email, "AccountType": acctType, "Password":password})
            auth.send_email_verification(user['idToken'])
            session['user'] = email
            session['name'] = name
            session['AccountType'] = acctType
            db.child("doctorPortal").child(idGivenEmail(email)).set({"Name":name, "Symptoms": "incomplete", "Diagnosis": "incomplete", "Question": "", "Date": "not scheduled", "Link": "not scheduled"})
            return redirect('/')
        else:
            db.child("doctorInfo").child(idGivenEmail(email)).set({"Names": name, "Email": email, "AccountType": acctType, "Password":password})
            return redirect('/signUp2/'+email)
@app.route("/signOut", methods=['GET', 'POST'])                   
def signOut():
    if 'user' not in session:
        return redirect('/')
    del session['user']
    del session['name']
    del session['AccountType']
    return redirect('/')

if __name__ == "__main__":        
    app.run()
                  

