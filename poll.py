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

def response(val):
    return response_data[val]

@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)

@app.route('/poll')
def poll():
    vote = request.args.get('field')
    vote_val = -1; 
    for val in range(0, 3):
        if vote == ANS_ENUM[val]:
            vote_val = val
            print(vote_val)
    if vote_val == -1:
        print("Error")
            
    str_response = response(vote_val)          

    out = open(filename, 'a')
    out.write( str(vote_val) + '\n' )
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
