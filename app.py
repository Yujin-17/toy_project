import bson
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@Cluster0.mhvqxjc.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta



@app.route('/')
def home():
    all_toy = list(db.toy.find({}))
    all_toy_ids = []
    all_toy_ids2 = []

    for value in all_toy:
        all_toy_ids.append(str(value['_id']))

    for value2 in all_toy:
        all_toy_ids2.append(value2['question_name'])
    print(all_toy_ids)
    print(all_toy_ids2)

    return render_template('index.html', all_toy_ids=all_toy_ids, all_toy_ids2=all_toy_ids2, zip=zip)


@app.route('/createQ')
def createQ():
    return render_template('createQ.html')


@app.route('/test')
def test():
    return render_template('test.html')

@app.route("/test", methods=["POST"])
def toyproject_post():
     userid_receive = request.form["userid_give"]
     userpw_receive = request.form["userpw_give"]

     doc = {
         'userid': userid_receive,
         'userpw': userpw_receive
     }

     db.toyproject.insert_one(doc)
     return jsonify({'msg':'문제만들기!'})

@app.route('/create',methods=["POST"])
def save():
    question_receive = request.form['question_give']
    num_receive = request.form['num_give']
    question_name_receive = request.form['question_name_give']
    question1_receive = request.form['question1_give']
    question2_receive = request.form['question2_give']
    question3_receive = request.form['question3_give']
    question4_receive = request.form['question4_give']

    # print(question_receive, num_receive, question_name_receive
    #       , question1_receive, question2_receive
    #       , question3_receive, question4_receive)

    doc = {
        'question':question_receive,
        'correctNum':num_receive,
        'question_name': question_name_receive,
        'question1':question1_receive,
        'question2': question2_receive,
        'question3': question3_receive,
        'question4': question4_receive,
    }
    db.toy.insert_one(doc)
    return jsonify({'msg':'답 저장 완료!'})


@app.route("/questions/<id>", methods=["GET"])
def find_one_question(id):
    question = db.toy.find_one({"_id": bson.ObjectId(oid=str(id))})
    question['_id'] = str(question['_id'])
    # print(question)
    return render_template('seoa.html', question=question)



@app.route("/questions/<id>/check", methods=["GET"])
def get_answer (id):
    question = db.toy.find_one({"_id": bson.ObjectId(oid=str(id))})
    question['_id'] = str(question['_id'])
    print(question)
    answer_list = question['correctNum']

    return jsonify({'answer': answer_list})




if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)

