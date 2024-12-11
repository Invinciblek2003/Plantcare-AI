import os
from flask import Flask, redirect, render_template, request, jsonify
from PIL import Image
import torchvision.transforms.functional as TF
from flask import Flask, redirect, render_template, request, url_for, flash
import CNN
import numpy as np
import torch
import pandas as pd

# Load data and model
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')

model = CNN.CNN(39)  # Replace with actual CNN model initialization if needed
#model.load_state_dict(torch.load("plant_disease_model_1.pt"))
model.load_state_dict(torch.load("plant_disease_model_1.pt", map_location=torch.device('cpu'), weights_only=True))
model.eval()

# Function to make predictions
def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))  # Resize to model's expected input size
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

app.secret_key = 'your_secret_key'  # Required for flash messages

# Fixed username and password
USERNAME = "jspm"
PASSWORD = "jspm"

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/templates/contact.html')
def contact():
    return render_template('contact.html')

"""@app.route('/templates/login.html')
def login():
    return render_template('login.html')"""

@app.route('/templates/explore.html')
def ai_engine_page():
    return render_template('explore.html')

@app.route('/templates/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate user
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('home_page'))  # Redirect to index.html
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')  # Render login page

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['plantImage']
        if image:
            filename = image.filename
            file_path = os.path.join('static/uploads', filename)
            image.save(file_path)
            print(f"Image saved to {file_path}")

            # Run prediction
            pred = prediction(file_path)
            title = disease_info['disease_name'][pred]
            description = disease_info['description'][pred]
            prevent = disease_info['Possible Steps'][pred]
            image_url = disease_info['image_url'][pred]
            supplement_name = supplement_info['supplement name'][pred]
            supplement_image_url = supplement_info['supplement image'][pred]
            supplement_buy_link = supplement_info['buy link'][pred]

            # Render the result page with the prediction data
            return render_template('submit.html', title=title, desc=description, prevent=prevent,
                                   image_url=image_url, pred=pred, sname=supplement_name,
                                   simage=supplement_image_url, buy_link=supplement_buy_link)

    return redirect('/index.html')

if __name__ == '__main__':
    app.run(debug=True)
