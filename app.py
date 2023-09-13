from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, login_required

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the Tree model
class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __init__(self, name, species, age, description):
        self.name = name
        self.species = species
        self.age = age
        self.description = description


users = []


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists
        for user in users:
            if user['username'] == username:
                return "<h1>Username already exists. Please try a different username.</h1>"

        # If username is unique, add the user to the list
        users.append({'username': username, 'password': password})
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and password matches
        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect(url_for('home', username=username))

        return "<h1>Invalid credentials. Please try again.</h1>"

    return render_template('login.html')


@app.route('/')
def home():
    return render_template('home.html')


# Route to display the form to add a new tree and handle form submission
@app.route('/add_tree', methods=['GET', 'POST'])
def add_tree():
    if request.method == 'POST':
        # Handle the form submission and add the tree to the database
        name = request.form['name']
        species = request.form['species']
        age = int(request.form['age'])
        description = request.form['description']

        new_tree = Tree(name=name, species=species, age=age, description=description)
        db.session.add(new_tree)
        db.session.commit()

        flash('Tree added successfully!', 'success')
        return redirect(url_for('view_trees'))

    # If the request method is GET, show the form to add a new tree
    return render_template('booknow.html')


@app.route('/view_trees')
def view_trees():
    trees = Tree.query.all()
    return render_template('view.html', trees=trees)


@app.route('/edit/<int:id>', methods=['GET'])
def show_edit_tree_form(id):
    tree = Tree.query.get_or_404(id)
    return render_template('edit.html', tree=tree)


# Route to handle the form submission and update an existing tree
@app.route('/edit/<int:id>', methods=['POST'])
def edit_tree(id):
    if request.method == 'POST':
        tree = Tree.query.get_or_404(id)

        tree.name = request.form['name']
        tree.species = request.form['species']
        tree.age = int(request.form['age'])
        tree.description = request.form['description']

        db.session.commit()
        flash('Tree updated successfully!', 'success')
        return redirect(url_for('view_trees'))

    return redirect(url_for('view_trees'))


@app.route('/logout')
def logout():
    return render_template('logout.html')


# Route to delete a tree from the database
@app.route('/delete/<int:id>', methods=['POST'])
def delete_tree(id):
    tree = Tree.query.get_or_404(id)
    db.session.delete(tree)
    db.session.commit()

    flash('Tree deleted successfully!', 'success')
    return redirect(url_for('view_trees'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Here, you can add code to process the form data or save it to a database
    return render_template('thank_you.html', name=name)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
