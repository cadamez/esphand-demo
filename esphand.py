from flask import Flask, render_template, request, session, redirect, url_for, escape
from datetime import date, timedelta
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=escape(session['username'])) 
    else:
        return redirect(url_for('login'))

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

@app.route("/sections/<sectionname>/edit")
def edit_section(sectionname):
	return render_template("arrange_section.html")

#@app.route('/')
#def index():

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('dashboard'))
    return '''
        <form action="" method="post">
            <p><label>Username:</label><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
	app.run(debug=bool(os.getenv('FLASK_DEBUG', False)))
