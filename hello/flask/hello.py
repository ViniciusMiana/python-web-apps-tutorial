from flask import Flask
app = Flask(__name__)

@app.route("/<data>")
@app.route("/", defaults={'data' : ''})
def hello(data):
   return "Hello "+data

if __name__ == "__main__":
   app.run()

