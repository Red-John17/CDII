# from flask import Flask, render_template, request, redirect, url_for, flash, send_file
# from flask_cors import CORS, cross_origin
# import os
# import json

# app = Flask(__name__)
# CORS(app, support_credentials=True)

# @app.route('/')
# @cross_origin(supports_credentials=True)
# def index():
#     return "Index Page"

# @app.route('/upload', methods=['POST'])
# @cross_origin(supports_credentials=True, origins='*')
# def upload():
#     if request.method != 'POST':
#         return 'Invalid request'
        
#     f = request.files['file']
#     f.save(f'uploads/{f.filename}')
#     return 'file uploaded successfully'

# @app.route('/convert', methods=['POST'])
# @cross_origin(supports_credentials=True, origins='*')
# def convert_graph():
#     if request.method != 'POST':
#         return 'Invalid request'

#     fname = request.json['fname']
#     type = request.json['type']
#     # run graph converter
#     os.system(f'python graphConverter.py -i uploads/{fname} -o uploads/ -t {type} -n {fname.split(".")[0]}')
#     # delete file from uploads
#     os.remove(f'uploads/{fname}')
    
#     # return file name as json
#     return {'fname': f'{fname.split(".")[0]}.graphml'}

# @app.route('/community', methods=['POST'])
# @cross_origin(supports_credentials=True)
# def community_detection():
#     if request.method != 'POST':
#         return 'Invalid request'

#     fname = request.json['fname']
#     try:
#         algo = request.json['algo']
#     except:
#         algo = 'louvain'
    
#     # run community detection
#     os.system(f'python graphActions.py -i uploads/{fname} -o uploads/{fname} -c -a {algo}')
#     os.system(f'python3 src/ghraphml-to-json.py uploads/{fname}')
#     return 'community detection completed'

# @app.route('/influencers', methods=['POST'])
# @cross_origin(supports_credentials=True)
# def influencer_identification():
#     if request.method != 'POST':
#         return 'Invalid request'

#     fname = request.json['fname']
#     # run influencer identification
#     os.system(f'python graphActions.py -i uploads/{fname} -o uploads/{fname} -in')
#     return 'influencer identification completed'

# @app.route('/export', methods=['GET'])
# @cross_origin(supports_credentials=True)
# def export():
#     if request.method != 'GET':
#         return 'Invalid request'

#     fname = request.args.get('fname')
    
#     # change extension to json 
#     fname = f'{fname.split(".")[0]}.json'
#     # send the json content of file back as json
    
#     f = open(f'uploads/{fname}', 'r')
#     content = json.load(f)
#     f.close()
    
#     return content

from flask import Flask, render_template, request, send_file
from flask_cors import CORS, cross_origin
import os
import json

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
@cross_origin(supports_credentials=True)
def index():
    return render_template('index.html')

@app.route('/upload_csv', methods=['POST'])
@cross_origin(supports_credentials=True, origins='*')
def upload_csv():
    if request.method != 'POST':
        return 'Invalid request'
        
    f = request.files['csv_file']
    f.save(f'uploads/{f.filename}')
    return 'CSV file uploaded successfully'

@app.route('/convert_and_download', methods=['GET'])
@cross_origin(supports_credentials=True)
def convert_and_download():
    if request.method != 'GET':
        return 'Invalid request'

    fname = request.args.get('fname')
    graph_type = request.args.get('type', 'default')

    # Run graph conversion
    os.system(f'python graphConverter.py -i uploads/{fname} -o uploads/ -t {graph_type} -n {fname.split(".")[0]}')

    # Run community detection
    os.system(f'python graphActions.py -i uploads/{fname} -o uploads/{fname} -c')

    # Run influencer identification
    os.system(f'python graphActions.py -i uploads/{fname} -o uploads/{fname} -in')

    # Convert GraphML to JSON
    os.system(f'python3 src/ghraphml-to-json.py uploads/{fname}')

    # Read JSON content
    with open(f'uploads/{fname.split(".")[0]}.json', 'r') as f:
        content = json.load(f)

    # Return JSON content as a downloadable file
    return send_file(f'uploads/{fname.split(".")[0]}.json', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
