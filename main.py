from flask import Flask, render_template, redirect, request
import pyrebase

app = Flask(__name__)   

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
userDatabase = firebase.FirebaseApplication('https://hackforafrica.firebaseio.com/inventoryData')

@app.route("/")                   
def home():  
    return render_template('home.html')

@app.route("/askQuestions", methods=['GET', 'POST'])                   
def askQuestions():               
	if request.method == 'GET':
	    return render_template('askQuestions.html')
	else:
		searchText = request.form['search']
		return searchText

#        prod_var = {"Store":prodStore, "Name":prodName, "Price":prodPrice, "Size":prodSize, "Quantity":prodQuantity}
#        db.child("inventoryData").child(str(prodStore+prodName+prodSize)).set(prod_var)


@app.route("/answerQuestions")                   
def answerQuestions():                     
    return render_template('answerQuestions.html')

@app.route("/schedule")                   
def schedule():                     
    return render_template('schedule.html')

if __name__ == "__main__":        
    app.run()                     