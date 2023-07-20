
from flask import Flask
from flask import render_template

app = Flask(__name__)
'''
@app.before_first_request
def before_first_request():
    app.logger.info("before_first_request")
 '''
 


@app.route("/")
def main():
    app.logger.info("main route")
    return render_template('index.html')
  
# run the application
if __name__ == "__main__":
    main()
    app.run(debug=True)

    