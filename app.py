from flask import Flask
from flask import request, Response, render_template, redirect, url_for, send_file
import get_image
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

#Change this path when running on your system if needed. Database is in the current working directory.
engine = sqlalchemy.create_engine('sqlite:///cve')

app = Flask(__name__)

# disable cache
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/styleGuide")
def styles():
    return render_template("styleGuide.html")

@app.route("/vendors")
def vendors():
    return render_template("byVendor.html")

@app.route("/products")
def products():
    return render_template("byProduct.html")


@app.route("/api/v1/query", methods=["GET", "POST"])
def query():
    out = ""
    if request.method == "POST":
        if request.form["query"]:
            query = request.form["query"]
            Session = scoped_session(sessionmaker(bind=engine))
            s = Session()
            try:
                # ooooo scaryyy! FIXME: sanitize/escape user input!!!
                print(query)
                result = s.execute(query)
                print(result)
                # iterate through results
                for item in result:
                    #print(item)
                    out = out + str(item) + " \n"
                print("Query Successful.")
                return out

            except:
                print("Query Failed.")
                return "Invalid SQL Statement or SQL error."
        else:
            return "No Query."

    else:
        return ">:("



if __name__ == '__main__':
    Flask.run(app, port="7777", debug=True)
