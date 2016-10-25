from flask import Flask, render_template, request
import os
app = Flask(__name__)


ANS_ENUM = ['No', 'Unfamiliar with Drink', 'Yes']
response_data = ['You should try bacardi and coke', 'You should try vodka martini', 'You should try mimosa']





poll_data =[
    {'question' : 'Do you like Whiskey and Coke?',
   'fields'   : ['Yes', 'No', 'Unfamiliar with Drink'], 'val' : 'q0'},

   {'question' : 'Do you like Long Island?',
   'fields'   : ['Yes', 'No', 'Unfamiliar with Drink'], 'val' : 'q1'},

   {'question' : 'Do you like Gin and Tonic?',
   'fields'   : ['Yes', 'No', 'Unfamiliar with Drink'], 'val' : 'q2'}]
filename = 'data.txt'

def response(val0, val1, val2):
    return response_data[val0 + 1]

@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)

@app.route('/poll')
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
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0

    f  = open(filename, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1

    return render_template('results.html', data=poll_data, votes=votes)



if __name__ == "__main__":
    app.run(debug=True)
