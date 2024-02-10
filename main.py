from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastai.vision.all import *
from fastapi.responses import HTMLResponse
import shutil
import os
from jinja2 import Template
import pathlib


plt = platform.system()
if plt == 'Linux': pathlib.WindowsPath = pathlib.PosixPath


app = FastAPI()
templates = Jinja2Templates(directory="templates")


API_KEY = "475DfF8s6joR3pve5606"

def get_api_key(api_key: str = Form(...)):
    if api_key == API_KEY:
        return True
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    html_content = """
    <!DOCTYPE html>
<html>
<head>
  <title>Определение материала объекта</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #FFFFFF;
      text-align: center;
      padding: 20px;
    }

    h1 {
      color: #57595B;
    }

    h2 {
      color: #57595B;
    }

    input[type=file],
    input[type=text],
    input[type=submit] {
      padding: 10px;
      margin-bottom: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 16px;
    }

    input[type=file] {
      padding: 30px;
      margin-bottom: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 16px;
      background-color: #FFFFFF;
    }

    input[type=submit] {
      background-color: #E1DBD8;
      color: #57595B;
      border: none;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    input[type=submit]:hover {
      background-color: #9B8579;
      color: #FFFFFF;
      transition: background-color 0.3s;
    }
  </style>

  <script>
    window.onload = function() {
      var dropArea = document.getElementById('file');

      dropArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropArea.style.backgroundColor = '#e2e2e2';
      });

      dropArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropArea.style.backgroundColor = '';
      });

      dropArea.addEventListener('drop', function(e) {
        e.preventDefault();
        dropArea.style.backgroundColor = '';
        var file = e.dataTransfer.files[0];
        var input = document.getElementById('file');
        input.files = e.dataTransfer.files;
        input.value = file.name;
      });
    };
  </script>
</head>
<body>
  <h1>Система рекомендаций по заполнению полей метаданных археологических объектов</h1>
  <form action="/classify" method="post" enctype="multipart/form-data">
    <label for="file">Загрузить изображение:</label><br>
    <input type="file" id="file" name="file"><br>
    <label for="api_key">Ключ доступа:</label><br>
    <input type="text" id="api_key" name="api_key"><br><br>
    <input type="submit" value="Получить результат">
  </form>

  </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post('/classify')
async def classify(request: Request, file: UploadFile = File(...), api_key: str = Form(...), authorized: bool = Depends(get_api_key)):
    if not file:
        raise HTTPException(status_code=400, detail="File not found")
    temp_file = f"tempfile.{file.filename.split('.')[-1]}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    learner = load_learner("app/model.pkl")
    result = learner.predict(temp_file)

    name_pred = str(result[1])
    name_pred = int(name_pred[name_pred.find('(')+1:name_pred.find(')')])
    perc_pred = str(result[2][name_pred])
    perc_pred = round(float(perc_pred[perc_pred.find('(')+1:perc_pred.find(')')]),2)

    if result[0] == 'бронза':
        tech = 'литье'
    elif result[0] == 'глина':
        tech = 'лепка'
    elif result[0] == 'железо':
        tech = 'ковка'
    elif result[0] == 'камень':
        tech = 'скалывание'
    elif result[0] == 'керамика':
        tech = 'лепка'
    elif result[0] == 'кость':
        tech = 'резьба'
    elif result[0] == 'медь':
        tech = 'литье'

    os.remove(temp_file)


    material = result[0]
    technique = tech
    probability = f"{round(perc_pred * 100, 0)}%"


    html_content = """
    <!DOCTYPE html>
<html>
<head>
  <title>Определение материала объекта</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #FFFFFF;
      text-align: center;
      padding: 20px;
    }

    h1 {
      color: #57595B;
    }

    h2 {
      color: #57595B;
    }

    input[type=file],
    input[type=text],
    input[type=submit] {
      padding: 10px;
      margin-bottom: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 16px;
    }

    input[type=file] {
      padding: 30px;
      margin-bottom: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      font-size: 16px;
      background-color: #FFFFFF;
    }

    input[type=submit] {
      background-color: #E1DBD8;
      color: #57595B;
      border: none;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    input[type=submit]:hover {
      background-color: #9B8579;
      color: #FFFFFF;
      transition: background-color 0.3s;
    }
  </style>

  <script>
    window.onload = function() {
      var dropArea = document.getElementById('file');

      dropArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropArea.style.backgroundColor = '#e2e2e2';
      });

      dropArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropArea.style.backgroundColor = '';
      });

      dropArea.addEventListener('drop', function(e) {
        e.preventDefault();
        dropArea.style.backgroundColor = '';
        var file = e.dataTransfer.files[0];
        var input = document.getElementById('file');
        input.files = e.dataTransfer.files;
        input.value = file.name;
      });
    };
  </script>
</head>
<body>
  <h1>Система рекомендаций по заполнению полей метаданных археологических объектов</h1>
  <form action="/classify" method="post" enctype="multipart/form-data">
    <label for="file">Загрузить изображение:</label><br>
    <input type="file" id="file" name="file"><br>
    <label for="api_key">Ключ доступа:</label><br>
    <input type="text" id="api_key" name="api_key"><br><br>
    <input type="submit" value="Получить результат">
  </form>



  <div id="result">

    {% if material %}

    <h2>Результат:</h2>
    <p>Материал: <b>{{ material }}</b><br> Техника: <b>{{ technique }}</b><br> Вероятность: <b>{{ probability }}</b></p>
    {% endif %}
  </div>
</body>
</html>

    """


    template = Template(html_content)

    variables = {
    'material': material,
    'technique': technique,
    'probability': str(round(perc_pred*100))+'%'
}

    return HTMLResponse(content=template.render(**variables), status_code=200)


