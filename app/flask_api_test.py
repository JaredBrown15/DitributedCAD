# using flask_restful
from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import wala_run
from flask_cors import CORS
import threading
import uuid


# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)
# CORS(app, origins=["https://jaredwjbrown.com", "https://www.jaredwjbrown.com"])
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": ["https://jaredwjbrown.com", "https://www.jaredwjbrown.com"]}})


jobs = {}


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/submission')
def submission():
    return render_template('submission.html')

@app.route('/model_info')
def model_info():
    return render_template('model_info.html')

@app.route('/my_info')
def my_info():
    return render_template('my_info.html')



# Background worker function
def run_wala_task(user_input, job_id):
    result = wala_run.main(user_input) 
    jobs[job_id] = {"status": "done", "result": result}

class WaLa(Resource):

    def post(self):
        data = request.get_json()
        user_input = data.get('prompt')
        # payload = wala_run.main(user_input)
        # return jsonify(payload)
        # Create unique job ID
        job_id = str(uuid.uuid4())
        jobs[job_id] = {"status": "pending", "result": None}

        thread = threading.Thread(target=run_wala_task, args=(user_input, job_id))
        thread.start()

        # Immediately return 202 Accepted
        # return jsonify({"status": "accepted", "job_id": job_id}), 202
        return ({"status": "accepted", "job_id": job_id}), 202

api.add_resource(WaLa, '/api')

# Polling endpoint to get JSON result
@app.route("/api/result/<job_id>")
def get_result(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job ID not found"}), 404
    if job["status"] != "done":
        return jsonify({"status": job["status"]}), 202
    return jsonify({"status": "done", "result": job["result"]})


# driver function
if __name__ == '__main__':
    # For local testing
    # app.run(debug=True, host='127.0.0.1', port=8000)
    # For docker
    app.run(debug=True, host='0.0.0.0', port=8000)