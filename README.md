# Point Cloud Processor

Point Cloud Processor is a Flask-based web application that allows users to process and visualize point cloud data. It supports various file formats and provides an easy-to-use interface for converting and viewing point clouds.

## Features

- Convert E57 files to LAS format
- Process LAS files into viewable point clouds
- Direct viewing of existing point cloud data
- Web-based 3D visualization using Potree

## Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.x
- Flask
- pylas
- numpy
- laspy
- PotreeConverter (command-line tool)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Cobalt9000/Point-Cloud-Processor.git
   cd point-cloud-processor
   ```

2. Install the required Python packages:
   ```
   pip install flask pylas numpy laspy
   ```

3. Install PotreeConverter and ensure it's available in your system PATH.

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Use the web interface to upload and process your point cloud files:
   - Option 1: Convert E57 to LAS and generate a point cloud
   - Option 2: Process an existing LAS file into a point cloud
   - Option 3: View an existing point cloud

4. After processing, you'll receive a URL to view the 3D visualization of your point cloud.

## File Structure

- `app.py`: The main Flask application
- `index.html`: The front-end interface
- `uploads/`: Temporary storage for uploaded files
- `potree_output/`: Output directory for processed point clouds
- `viewer/`: Directory for the Potree viewer files

## API Endpoints

- `/process` (POST): Handles file uploads and processing
- `/view/<path:filename>` (GET): Serves the Potree viewer files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Acknowledgements

This project uses the following open-source software:
- [Flask](https://flask.palletsprojects.com/)
- [pylas](https://github.com/tmontaigu/pylas)
- [laspy](https://github.com/laspy/laspy)
- [Potree](https://github.com/potree/potree)

