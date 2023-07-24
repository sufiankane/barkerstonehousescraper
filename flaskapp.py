from flask import Flask, render_template
import main

app = Flask(__name__, static_folder='/')

dataframe = 0


@app.route('/')
def hello_world(): #renders the page, needs jinja soon
   return render_template('index.html', table=dataframe)

if __name__ == '__main__':
   dataframe = main.main() #runs the webscraper when the app is started
   app.run(host='0.0.0.0', port=8080)