from run import app, Task, TaskSchema, ma, db
from datetime import datetime
from flask import jsonify, request

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/data')
def return_data():
    start_date = datetime.strptime(request.args.get('start', ''), '%Y-%m-%d')
    end_date = datetime.strptime(request.args.get('end', ''), '%Y-%m-%d')

    filtered_tasks = db.session.query(Task.completedate > start_date, Task.completedate < end_date).all()
    result = tasks_schema.dump(filtered_tasks).data

    task_list = []
    for i in result:
        if i['category'] == 'To Do':
            task_list.append({'id': i['id'], 'title': i['taskname'], 'start': i['completedate'], 'color': '#1aa3ff'})
        elif i['category'] == 'Doing':
            task_list.append({'id': i['id'], 'title': i['taskname'], 'start': i['completedate'], 'color': '#ff6666'})
        else:
            task_list.append({'id': i['id'], 'title': i['taskname'], 'start': i['completedate'], 'color': '#00b33c'})

    return jsonify(task_list)