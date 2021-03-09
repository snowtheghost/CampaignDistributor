from flask import Flask, render_template, url_for
app = Flask(__name__)


posts = [
    {
        'author': 'Justin Chan',
        'title': ' Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Example Author',
        'title': 'Post 2',
        'content': 'Example post content',
        'date_posted': 'April 21, 2018'
    }
]


# Specifies the web directory, in this case, the root/homepage
@app.route('/')
@app.route('/home')  # multiple decorators handled by the same function
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


if __name__ == '__main__':
    app.run(debug=True)  # Debug mode for development
