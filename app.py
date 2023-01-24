from flask import Flask, render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)


class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    year=db.Column(db.Integer)
    def __repr__(self):
        return f"{self.name}-{self.year}"

# @app.route('/',methods=['GET','POST'])
# def index():
#     if(request.method=='GET'):
#         return jsonify({'msg':'Hi'})

@app.route('/students',methods=['GET','POST'])
def students():
    if request.method=='GET':
        all_students=Student.query.all()
        output=[]
        for student in all_students:
            new_student={'id':student.id,'name':student.name,'year':student.year}
            output.append(new_student)
        return output
    else:
        data=request.get_json()
        db.session.add(Student(name=data['name'],year=data['year']))
        db.session.commit()
        return f"{data['name']} inserted successfully"

@app.route('/students/<int:id>',methods=['GET'])
def get_student(id):
    foundstudent=Student.query.get(id)
    if foundstudent is None:
        return {'error':'Not Found'}
    return {'name':foundstudent.name,'year':foundstudent.year}

@app.route('/students/<int:id>',methods=['PUT'])
def update_student(id):
    data=request.get_json()
    foundstudent=Student.query.get(id)
    if foundstudent is None:
        return {'error':'Not found'}
    foundstudent.name=data['name']
    foundstudent.year=data['year']
    db.session.commit()
    return data

@app.route('/students/<int:id>',methods=['DELETE'])
def delete_student(id):
    foundstudent=Student.query.get(id)
    if foundstudent is None:
        return {'error':'Not Found'}
    db.session.delete(foundstudent)
    db.session.commit()
    return f"{foundstudent.name} deleted successfully"

if __name__=='__main__':
    app.run(debug=True)