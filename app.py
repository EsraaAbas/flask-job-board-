from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_jwt_extended import JWTManager, jwt_required
from flask import request, jsonify
from flask_wtf.csrf import CSRFProtect


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


# lab 3 add CRUD operations-----------

# GET all companies
@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Job.query.all()
    return jsonify([c.to_dict() for c in companies]), 200

# GET single company
@app.route('/api/companies/<int:id>', methods=['GET'])
def get_company(id):
    company = Job.query.get_or_404(id)
    return jsonify(company.to_dict()), 200

#  Create new company (authenticated users only)
@app.route('/api/companies', methods=['POST'])
@jwt_required()
def create_company():
    data = request.get_json()
    new_company = Job(
        name=data['name'],
        description=data['description'],
        employees_count=data.get('employees_count', 0),
        location=data['location']
    )
    db.session.add(new_company)
    db.session.commit()
    return jsonify({"message": "Company created successfully!"}), 201

#  Update a company (authenticated users only)
@app.route('/api/companies/<int:id>', methods=['PUT'])
@jwt_required()
def update_company(id):
    company = Job.query.get_or_404(id)
    data = request.get_json()
    company.name = data['name']
    company.description = data['description']
    company.employees_count = data.get('employees_count', company.employees_count)
    company.location = data['location']
    db.session.commit()
    return jsonify({"message": "Company updated successfully!"}), 200

#  Delete a company (authenticated users only)
@app.route('/api/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    company = Job.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return jsonify({"message": "Company deleted successfully!"}), 200

class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    employees_count = StringField('Employees Count')
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Company')



if __name__ == '__main__':
    
   
    app.run(debug=True)