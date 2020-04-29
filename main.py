from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bme680')
def bme680():
	return render_template('bme680.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')