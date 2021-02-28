from flask import Flask, make_response, jsonify, request
from flask_mongoengine import MongoEngine
from datetime import datetime

app = Flask(__name__)

database_name = "API"
DB_URI ="mongodb+srv://arjit:pwd@cluster0.sl9zz.mongodb.net/API?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

class Project(db.Document):
    project_id = db.IntField()
    title = db.StringField()
    author = db.StringField()
    mentor = db.StringField()
    date = db.DateField()
    content = db.StringField()

    def to_json(self):

        return {
            "project_id": self.project_id,
            "title": self.title,
            "author": self.author,
            "mentor": self.mentor,
            "date": self.date,
            "content": self.content
        }

# @app.route("/api/db_populate", methods=["POST"])
# def db_populate():
#     project1 = Project(project_id=1, title="GAME OF THRONES", author="GEORGE R. MARTIN", mentor="A. YADAV", date=datetime.now(), content="Good project. wonderful")
    
#     project1.save()

#     return make_response("", 201)

@app.route("/api/projects", methods=["GET","POST"])
def api_projects():
    if request.method == "GET":
        projects = []
        for project in Project.objects:
            projects.append(project)
        return make_response(jsonify(projects), 200)

    elif request.method == "POST":
        content =request.json
        project = Project(
            project_id=content['project_id'],
            title=content['title'],
            author=content['author'],
            mentor=content['mentor'],
            date=datetime.now(),
            content=content['content']
        )
        project.save()
        return make_response("",201)

@app.route("/api/projects/<project_id>", methods=["GET", "PUT", "DELETE"])
def api_each_project(project_id):
    if request.method == "GET":
        project_obj=Project.objects(project_id=project_id).first()
        if project_obj:
            return make_response(jsonify(project_obj.to_json()),200)
        else:
            return make_response("",404)

    elif request.method == "PUT":
        content = request.json
        project_obj=Project.objects(project_id=project_id).first()
        project_obj.update(mentor=content['mentor'], content =content['content'])
        return make_response("",204)

    elif request.method == "DELETE":
        project_obj=Project.objects(project_id=project_id).first()
        project_obj.delete()
        return make_response("",204)

if __name__ == '__main__':
    app.run(debug=True)
