from flask import Flask, render_template, request, session, redirect, url_for, escape, flash
from datetime import date, timedelta
import os, random

app = Flask(__name__)

class DummyArticle(object):
    def __init__(self, **kwargs):
        self.title = kwargs['title'] or ''
        self.content = kwargs['content'] or ''
        self.revision_ids = kwargs['revision_ids'] if 'revision_ids' in kwargs else []
        self.locked = kwargs['locked'] if 'locked' in kwargs else False
        self.comments = kwargs['comments'] if 'comments' in kwargs else 0

@app.route("/")
def dashboard():
    if 'username' in session:
        if 'writer_stories' not in session:
            session['writer_stories'] = example_stories() 
        username=escape(session['username'])
        template_name = "dashboard_for_%s.html" % username
        print(session['writer_stories'])
        return render_template(template_name,
                                username=username,
                                upcoming_stories=session['writer_stories']) 
    else:
        return redirect(url_for('login'))

@app.route("/upcoming")
def upcoming():
    return render_template('upcoming.html') 

@app.route("/new")
def new_article():
    return render_template('new_article.html',
                            role=escape(session['username']),
                            story_is_locked=False,
                            story=DummyArticle(),
                            show_comments=False )
@app.route("/new", methods=['POST'])
def create_article():
    session['writer_stories'].append(DummyArticle(title=request.form['title'], content=request.form['content']))
    flash("Created article \"%s\"" % request.form['title'])
    return redirect(url_for('dashboard'))

@app.route("/story/<int:storyid>/edit", methods=['GET', 'POST', 'PATCH'])
def edit_article(storyid):
    form_action = "/story/%s/edit" % storyid
    if request.method == 'GET':
        story = session['writer_stories'][int(storyid)]
        username = escape(session['username'])
        todays_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        return render_template("new_article.html", story=story, username=username, role=username, action=form_action, story_is_locked=story.locked, todays_date=todays_date, show_comments=(story.comments > 0) )
    else:
        print(request.form)
        return redirect(url_for('dashboard'))

@app.route("/import")
def import_article():
    return render_template("import.html")
@app.route("/import", methods=['POST'])
def process_import():
    # Pretend to process that Word document here...
    word_doc_body = "Pretend that this text came from the Word document that you uploaded!!"
    return render_template('new_article.html', role=escape(session['username']), story_is_locked=False, story=DummyArticle(title=request.form['worddoc'], content=word_doc_body))

@app.route("/story/<int:storyid>/preview")
def preview_article():
    return render_template("preview.html")

@app.route("/sections/<sectionname>/edit")
def edit_section(sectionname):
    return render_template("arrange_section.html")

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
    #flash("You have logged out.")
    return redirect(url_for('dashboard'))

def example_stories():
    return [
            DummyArticle(title="Multi-tiered high-level structure for deploy wireless systems", content="This is some example content here", locked=True, revision_ids=[1,2,3], comments=random.randint(0, 20)),
            DummyArticle(title="Team-oriented reciprocal leverage on enhance B2C infrastructures", content="This is an example of content here as well", revision_ids=[1,2,3], comments=random.randint(0, 20)),
            DummyArticle(title="Crazy idea about cats in hats", content="Call the cat lady!!")
    ]

# set the secret key.  keep this really secret:
app.secret_key = os.getenv('FLASK_SEKRET_KEY')

if __name__ == "__main__":
    app.run(debug=bool(os.getenv('FLASK_DEBUG', False)))
