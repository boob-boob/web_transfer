from flask import Flask, send_file, render_template, request, redirect
from tkinter import filedialog

app = Flask(__name__)
download_path = ''

@app.route('/')
def index():
	return render_template('index.html', d_path=download_path)


@app.route('/download', methods=['GET'])
def download():
	if not download_path:
		return '<script>alert("Please select the file first.")</script>'
	else:
		return send_file(download_path)


@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	with open(file.filename, 'wb') as f:
		while True:
			chunk = file.read(10240)
			if not chunk:
				break
			f.write(chunk)
	return '<script>alert("Done.")</script>'


@app.route('/set_file_path')
def set_file_path():
	global download_path
	download_path = filedialog.askopenfilename()
	return redirect('/')


if __name__ == '__main__':
	app.run(host='0.0.0.0')
