
from flask import Flask, render_template, request
import pickle

#Here we are loading trained and tested Banking Model 
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

#Here we are loading trained and tested IT Support Model
with open("model_it_support.pkl", "rb") as model_file:
    model_it = pickle.load(model_file)

app = Flask(__name__)


#Here we are mapping prediction keywords to genarte a response for a support team
class_mapping = {0: 'credit_card', 1: 'credit_reporting', 2: 'debt_collection', 3: 'mortgages_and_loans', 4: 'retail_banking'}
class_mapping_it = {0: 'Hardware', 1: 'Access', 2: 'Miscellaneous', 3: 'HR Support', 4: 'Purchase', 5: "Administrative rights", 6: "Storage", 7: "Internal Project"}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict_banking', methods=['POST','GET'])
def predict_banking():
    if request.method == 'POST':
        user_query = request.form['query'] 
        try:
            prediction = model.predict([user_query])[0] 
            response = f"{class_mapping[prediction]} Team"
        except Exception as e:
            response = f"Error processing query: {str(e)}"
        return render_template('index_bank.html', response=response)
    return render_template('index_bank.html')

# Route to handle the form submission for IT support prediction and make predictions
@app.route('/predict_it', methods=['POST','GET'])
def predict_it():
    if request.method == 'POST':
        user_query = request.form['query']
        try:
            prediction = model_it.predict([user_query])[0]  
            print(prediction)
            response = f"{class_mapping_it[prediction]} Team"
        except Exception as e:
            response = f"Error processing query: {str(e)}"
        return render_template('index_it.html', response=response)
    return render_template('index_it.html')

if __name__ == '__main__':
    app.run(debug=True)
