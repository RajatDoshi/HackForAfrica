from flask import Flask, render_template, redirect, request, session
import json
import pyrebase

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
questionBank = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/questionBank')


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
		return render_template('land.html', signInStatus = "Sign Out")
	else: 
		return render_template('land.html')


@app.route("/diagnose", methods=['GET', 'POST'])                   
def askQuestions():               
	if request.method == 'GET':
		if 'user' in session:
			return render_template('askQuestions.html', signInStatus = "Sign Out")
		else:
			return redirect('/')
	else:
		searchText = request.form['search']

		questionDict = questionBank.get('/questionBank', idGivenEmail(session['user']))

		if questionDict != None:
			questionArr = questionDict['Question']
			questionArr.append(searchText)
			db.child("questionBank").child(idGivenEmail(session['user'])).set({"Question": questionArr})
		else:
			db.child("questionBank").child(idGivenEmail(session['user'])).set({"Question": [searchText]})
		
		return redirect('/diagnose#questionPage2')
		# return searchText

#        prod_var = {"Store":prodStore, "Name":prodName, "Price":prodPrice, "Size":prodSize, "Quantity":prodQuantity}
#        db.child("inventoryData").child(str(prodStore+prodName+prodSize)).set(prod_var)




@app.route("/doctorPortal")                   
def doctorsPortal():                     
	return render_template('doctorsPortal.html')

@app.route("/schedule")                   
def schedule():
	if 'user' in session:                  
		return render_template('schedule.html')
	else:
		return redirect('/signUp')


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

		if password != passwordRepeat:
			return render_template('createAccount.html', errorMessage="Passwords Do Not Match")
		try:
			user = auth.create_user_with_email_and_password(email, password)
		except Exception as e:
			fullErrorMessage = e.args[1]
			err = json.loads(fullErrorMessage)["error"]["message"]
			return render_template('createAccount.html', errorMessage=err)

		db.child("userInfo").child(idGivenEmail(email)).set({"Names": name, "Email": email, "AccountType": "User", "Password":password})
		auth.send_email_verification(user['idToken'])
		session['user'] = email
		return redirect('/')

@app.route("/signOut", methods=['GET', 'POST'])                   
def signOut():
    if 'user' not in session:
        return redirect('/')
    del session['user']
    return redirect('/')

if __name__ == "__main__":        
	app.run()                     