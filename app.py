from flask import Flask, request
from flask_json import FlaskJSON, json_response
from model import albert_qa

app = Flask(__name__)
FlaskJSON(app)

@app.route('/en', methods=['GET'])
def en_question_answering():
   try:
      context = request.json.get('context')
      question = request.json.get('question')
      answer = albert_qa.get_answer(context, question)
   except Exception as error:
      return json_response(status_=404, error=str(error))
   return json_response(status_=200, answer=answer)
