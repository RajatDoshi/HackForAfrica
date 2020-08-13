from flask import Flask, render_template, redirect, request, session
import json
import time
import pyrebase
import symptomClassifierAPI
from googlesearch import search

app = Flask(__name__)   

app.secret_key = '#d\xe9X\x00\xbe~Uq\xebX\xae\x82\x1fs\t\xb4\x99\xa3\x87\xe6.\xd1_'

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

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firebase.database()

from firebase import firebase
userDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/userInfo')
doctorPortalDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/doctorPortal')
doctorChat = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/doctorChat')
questionBank = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/questionBank')
diagnosisTableData = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/diagnosisTableData')

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
			return render_template('userLand.html', signInStatus = "Sign Out", acctType=session['AccountType'])
		else:
			return render_template('doctorLand.html', signInStatus = "Sign Out", acctType=session['AccountType'])
	else: 
		return render_template('land.html')	


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
				return render_template('diagnose.html', signInStatus = "Sign Out", symList=symList, tasks=tasks)
			else:
				return redirect('/')
		else:
			return redirect('/signUp')
	else:
		data = request.form.keys()
		symptomInput = []
		for sym in data:
			symptomInput.append(sym)
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

		# data = doctorPortalDatabase.get('/doctorPortal', idGivenEmail(session['user']))
		# data['Question'] = searchText
		# db.child("doctorPortal").child(idGivenEmail(session['user'])).set(data)		
		# return redirect('/diagnose#questionPage2')

@app.route("/scheduleDoctor")                   
def scheduleDoctor():  
	return render_template('scheduleDoctor.html')


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
				msgList.append({"Chat": msgDict["Chat"][i], "Time": msgDict["Time"][i], "Type": msgDict["Type"][i]})
		return render_template('chat.html', msgDict=msgList)
	else:
		return redirect('/signUp')

@app.route("/chatDoctor")                   
def chatDoctorGeneric():
	doctorChatDict = doctorPortalDatabase.get('/doctorChat', None)
	info = []
	for i,person in enumerate(doctorChatDict):
		lastChat = doctorChatDict[person]['Chat'][-1]
		info.append( {"Name": person, "Question": lastChat})
	return render_template('chatGeneric.html', tasks=info)

@app.route("/chatDoctor/<chattingWith>")                   
def chatDoctor(chattingWith):  
	msgDict = doctorPortalDatabase.get('/doctorChat', chattingWith)
	msgList = []
	if msgDict != None:
		for i in range(0, len(msgDict["Chat"])):
			msgList.append({"Chat": msgDict["Chat"][i], "Time": msgDict["Time"][i], "Type": msgDict["Type"][i]})
	return render_template('chatDoctor.html', msgDict=msgList, chattingWith=chattingWith)

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
	return render_template('doctorsPortal.html', tasks=doctorPortalList)
def getPortalInfo():
    portalDict = doctorPortalDatabase.get('/doctorPortal', None)
    portalList = []
    if portalDict != None:
        portalList = [value for value in portalDict.values()]
    return portalList

@app.route("/schedule", methods=['GET', 'POST'])                   
def schedule():
	if request.method == 'GET':
		if 'user' in session:                  
			return render_template('schedule.html')
		else:
			return redirect('/signUp')
	else:
		dateVal = "Aug 30th @ 1pm EST" #change to form value
		data = doctorPortalDatabase.get('/doctorPortal', idGivenEmail(session['user']))
		data['Date'] = dateVal
		data['Link'] = "https://yale.zoom.us/j/983"
		db.child("doctorPortal").child(idGivenEmail(session['user'])).set(data)	
		return redirect('/schedule')


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
		data['employeer'] = request.form['medicallicense']
		data['medSchoolName'] = request.form['medicallicense']
		data['years'] = request.form['years']
		db.child("doctorInfo").child(idGivenEmail(email)).set(data)
		
		session['user'] = email
		otherMetaData = userDatabase.get('/doctorInfo', idGivenEmail(email))
		session['name'] = otherMetaData['Names']
		session['AccountType'] = otherMetaData['AccountType']
		return redirect('/')


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
			db.child("doctorPortal").child(idGivenEmail(email)).set({"Name":name, "Symptoms": "", "Diagnosis": "", "Question": "", "Date": "", "Link": ""})
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