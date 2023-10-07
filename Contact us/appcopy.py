from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'noreply.artizence@gmail.com'
app.config['MAIL_PASSWORD'] = 'lnhhesnqycxkgdgh'           #16 DIGIT CODE..refer this https://stackoverflow.com/a/72553362/8396003
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(path.abspath(path.dirname(__file__)), 'data.sqlite')
app.config['SECRET_KEY'] = "random string"

mail = Mail(app)
db = SQLAlchemy(app)

class Contactus(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    message = db.Column(db.String(20000))
    subject = db.Column(db.String(200))
    phno = db.Column(db.String(12))

    def __init__(self, name, email, subject,message,phno):
        self.name = name
        self.email = email
        self.subject = subject
        self.phno = phno
        self.message = message

def sendContactForm(result):
    msg = Message("Thank You!",
                  sender="noreply.artizence@gmail.com",
                  recipients=[result['email']])

    msg.body = """
    Hello there,

    WE wil contact you soon regarding the query below.

    Name: {}
    Email: {}
    Message: {}
    subject: {}
    phno: {}



    regards,
    Admin

    """.format(result['name'], result['email'], result['message'],result['subject'],result['phno'])

    mail.send(msg)

    print("Success")



@app.route("/")
def hello():
    return "None"



@app.route("/contact", methods=["GET", "POST"])
@rule_documenter.define( 
path="/text", request={ 
    "type": "json", 
    "fields":
    { 
    "name":"The text to generate a response for." ,
    "email":"The text to generate a response for." ,
    "message":"The text to generate a response for." ,
    "subject":"The text to generate a response for." ,
    "phno":"The text to generate a response for." 
    } 
 }, 
response={ 
    "type": "json", 
    "data":
    {
    "name":"The text to generate a response for." ,
    "email":"The text to generate a response for." ,
    "message":"The text to generate a response for." ,
    "subject":"The text to generate a response for." ,
    "phno":"The text to generate a response for." 
    } 
}, 
methods=["GET", "POST"] 
)

def contact():
    f = request.get_json(force=True) 

    if request.method == 'POST':
        result = {}
        
        # result['name'] = f.get("name")
        # result['email'] = f.get("email").replace(' ', '').lower()
        # result['message'] = f.get("message")
        # result['subject'] = f.get("subject")
        # result['phno'] = f.get("phno")

        feild = Contactus(f.get("name"), f.get("email"), f.get("subject"), f.get("message"),f.get("phno"))
         
        db.session.add(feild)
        print("session completed")
        db.session.commit()

        sendContactForm(result)
        

        return render_template('contact.html', **locals())


    return render_template('contact.html', **locals())



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')


