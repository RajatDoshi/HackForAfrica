from flask import Flask, render_template, redirect

app = Flask(__name__)             

@app.route("/")                   
def home():                     
    return render_template('home.html')

@app.route("/askQuestions")                   
def askQuestions():                     
    return render_template('askQuestions.html')

@app.route("/answerQuestions")                   
def answerQuestions():                     
    return render_template('answerQuestions.html')



if __name__ == "__main__":        
    app.run()                     