from flask import Flask, render_template,flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import speech_
# import soundfile as sf 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    text=None
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        # print(os.path.join(os.path.abspath(os.path.dirname(__file__))))
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        text = speech_.speech2text(file.filename)
        flash(str(text))
    return render_template('index.html', form=form,text=text)

if __name__ == '__main__':
    app.run(debug=True)
