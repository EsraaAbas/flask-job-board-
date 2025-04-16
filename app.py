from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'soso' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Job(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    employees_count = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(300), nullable=False)








# form to add job ...............................
class jobCreationForm(FlaskForm):
    job_title= StringField('Title', validators=[DataRequired()])
    name = StringField('Company', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description=StringField('description', validators=[DataRequired()])
    id = StringField('job id', validators=[DataRequired()])


    submit = SubmitField('Create Job')


@app.route('/form', methods=['GET', 'POST'])
def create_job_form():
    form = jobCreationForm()
    
    if form.validate_on_submit():
        
        job_id = int(form.id.data)

        title = form.job_title.data
        company = form.name.data
        location = form.location.data
        description = form.description.data 

        new_job = Job(
            id=job_id,
            job_title=title,
            name=company,
            location=location,
            description=description
        )

        db.session.add(new_job)
        db.session.commit()

        return "Job created successfully!"
    
    print("Form errors:", form.errors)  

    return render_template('form.html', form=form)



# all jops..............
@app.route('/home')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

# specific job ................
@app.route('/job/<int:job_id>', methods=['GET']) 
def job_details(job_id):  
    job_instance = Job.query.get(job_id) 
    return render_template('job.html', job=job_instance) 

if __name__ == '__main__':
   
    app.run(debug=True)