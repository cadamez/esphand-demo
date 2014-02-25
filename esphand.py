from flask import Flask, render_template, request
from datetime import date, timedelta

app = Flask(__name__)

@app.route("/")
def dashboard():
	return render_template('dashboard.html') 

@app.route("/upcoming")
def upcoming():
	return render_template('upcoming.html') 

@app.route("/new")
def new_article():
	return render_template('new_article.html')
@app.route("/new", methods=['POST'])
def other():
	return str(request.form)

@app.route("/edit")
def edit_article():
	if request.args.get('lock', '') == 'true':
		template = 'locked.html'
	else:
		template = 'revisions.html'
	return render_template(template)

@app.route("/preview")
def preview_article():
	return render_template("preview.html")

if __name__ == "__main__":
	app.run(debug=True)
