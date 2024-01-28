
import sys
sys.path.append("/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024")
import json
from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from llama_index import SimpleDirectoryReader
from PIL import Image
from app.cv_submissions.main import get_details_from_multimodal_gemini

UPLOAD_FOLDER = '/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Init app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return "works like a charm"

@app.route('/doc', methods=['GET','POST'])
def uploadFile():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                img = Image.open(f"{os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
                img = img.resize((500, 500))
                img.save(f"{os.path.join(app.config['UPLOAD_FOLDER'], filename)}")

                print(f"{os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
                images_documents = SimpleDirectoryReader(
                    input_files=[f"{os.path.join(app.config['UPLOAD_FOLDER'], filename)}"]).load_data()
                
                print(images_documents)
                
                try:
                    response = get_details_from_multimodal_gemini(
                        uploaded_image=images_documents)
                    
                    # store processed information
                    with open("/home/mani1911/Documents/Pragyan-Hack/CTY-NOW-2024/app/cv_submissions/data/data_store.jsonl", "a") as f:
                        f.write(json.dumps({"doc": ', '.join(
                            [f"{key}: {value}" for key, value in response.items()])}) + "\n")
                        
                except Exception as e:
                    print(e)

                # response = get_details_from_multimodal_gemini(uploaded_image=images_documents)
                # print(response)
                return jsonify({"message": "successfully uploaded"})
        
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''


# A method that runs the application server.
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=False, threaded=True, port=7000)