from flask import Flask, render_template
import main

app = Flask(__name__)

@app.route('/')
def hello_world(): #renders the page, needs jinja soon
   return render_template('index.html')

if __name__ == '__main__':
   main.main() #runs the webscraper when the app is started
   app.run(port=8080)