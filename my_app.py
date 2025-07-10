from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
import joblib
import json
import os
import fitz 
import re
import nltk
nltk.download('punkt')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Загрузка модели и данных
model = load_model('my_model.keras')
vectorizer = joblib.load('my_vectorizer.pkl')
with open('categories.json') as f:
    categories = json.load(f)

# Функции предобработки
def extract_text(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def tokenize_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = nltk.word_tokenize(text.lower(), language='english')
    return ' '.join(tokens)

@app.route("/", methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        pdf = request.files['pdf']
        if pdf.filename.endswith('.pdf'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
            pdf.save(path)
            raw_text = extract_text(path)
            clean_text = tokenize_text(raw_text)
            vec = vectorizer.transform([clean_text])
            pred_class = model.predict(vec.toarray())
            predicted_index = pred_class.argmax(axis=1)[0]
            prediction = categories[predicted_index]
        else:
            prediction = 'Файл не в формате .pdf!'

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)