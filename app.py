import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory
import pylas
import numpy as np

from laspy.file import File

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
POTREE_OUTPUT_FOLDER = 'potree_output'
VIEWER_FOLDER = 'viewer'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(POTREE_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(VIEWER_FOLDER, exist_ok=True)

def convert_e57_to_las(input_file):
    try:
        # Attempt to open the E57 file with laspy
        e57_file = File(input_file, mode='r')

        # Create a new LAS file for writing
        output_file = os.path.splitext(input_file)[0] + '.las'
        las_file = File(output_file, mode='w', header=e57_file.header)

        # Copy the point data
        las_file.points = e57_file.points

        # Close both files
        e57_file.close()
        las_file.close()

        return output_file

    except Exception as e:
        # Handle potential errors during conversion
        print(f"Error converting E57 to LAS: {e}")
        return None  

def convert_las_to_pointcloud(input_file):
    output_dir = os.path.join(POTREE_OUTPUT_FOLDER, os.path.splitext(os.path.basename(input_file))[0])
    subprocess.run(["PotreeConverter", input_file, "-o", output_dir, "--generate-page", "index"])
    return output_dir

def setup_potree_viewer(input_directory):
    viewer_dir = os.path.join(VIEWER_FOLDER, os.path.basename(input_directory))
    os.makedirs(viewer_dir, exist_ok=True)
    subprocess.run(["cp", "-r", input_directory, viewer_dir])
    return f"/view/{os.path.basename(input_directory)}/index.html"

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    option = request.form.get('option', '1')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        if option == '1':
            las_file = convert_e57_to_las(file_path)
            if las_file:  # Check if conversion was successful
                pointcloud_dir = convert_las_to_pointcloud(las_file)
                viewer_url = setup_potree_viewer(pointcloud_dir)
            else:
                return jsonify({'error': 'E57 to LAS conversion failed'})
        elif option == '2':
            pointcloud_dir = convert_las_to_pointcloud(file_path)
            viewer_url = setup_potree_viewer(pointcloud_dir)
        elif option == '3':
            viewer_url = setup_potree_viewer(file_path)
        else:
            return jsonify({'error': 'Invalid option'})
        
        return jsonify({'viewer_url': viewer_url})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/view/<path:filename>')
def serve_viewer(filename):
    return send_from_directory(VIEWER_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)