from flask import Flask, render_template, request, Response, redirect, url_for, session, abort
from flask.ext.login import LoginManager, UserMixin, \
login_required, login_user, logout_user
import os
import lookup

app = Flask(__name__)


ANS_ENUM = ['No', 'Unfamiliar with Drink', 'Yes']
response_data = ['You should try bacardi and coke', 'You should try vodka martini', 'You should try mimosa']

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]

poll_data =[
    {'question' : 'Do you like Whiskey and Coke?',
   'fields'   : ['Yes', 'No', 'Unfamiliar with Drink'], 'val' : 'q0'},

   {'question' : 'Do you like Long Island?',
   'fields'   : ['Yes', 'No', 'Unfamiliar with Drink'], 'val' : 'q1'},

   {'question' : 'Do you like Gin and Tonic?',
   'fields'   : ['Yes', 'No', 'Unfamiliar with Drink'], 'val' : 'q2'}]
filename = 'data.txt'

def response(val0, val1, val2):
    tup = (val0, val1, val2)

    return lookup.ginWhiskeyTeaTable[tup]

@app.route('/')
@login_required
def root():
    return render_template('poll.html', data=poll_data)

@app.route('/poll')
@login_required
def poll():
    vote0 = request.args.get('q0')
    vote1 = request.args.get('q1')
    vote2 = request.args.get('q2')
    vote_val0 = -2
    vote_val1 = -2
    vote_val2 = -2
    print(vote0)
    for val in range(0, 3):
        if vote0 == ANS_ENUM[val]:
            vote_val0 = val-1
            print(vote_val0)
    if vote_val0 == -1:
        print("Error")

    for val in range(0, 3):
        if vote1 == ANS_ENUM[val]:
            vote_val1 = val-1
            print(vote_val1)
    if vote_val1 == -1:
        print("Error")

    for val in range(0, 3):
        if vote2 == ANS_ENUM[val]:
            vote_val2 = val-1
            print(vote_val2)
    if vote_val2 == -1:
        print("Error")

    str_response = response(vote_val0, vote_val1, vote_val2)


    out = open(filename, 'a')
    out.write( str(vote_val0) + '\n' )
    out.close()

    return render_template('thankyou.html', data=str_response)

@app.route('/results')
@login_required
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0

    f  = open(filename, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1

    return render_template('results.html', data=poll_data, votes=votes)



# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

if __name__ == "__main__":
    app.run(debug=True)
