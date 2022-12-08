from flask import Flask
from flask import request, Response, render_template, redirect, url_for, send_file
import get_image
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

# too lazy to make a seperate file for util functions

def xor(search_keys):
    out = ""
    base_query = '''select ci.cve_id, cvp.vendor, cp.vulnerable_product from cveitems as ci, `cve-vendors-products` as cvp, `cve-products` as cp where '''
    for key in search_keys:
        out = out + '''cp.vulnerable_product like "%{}%" or '''.format(key)
        out = out + ''' cvp.vendor like "%{}%" or '''.format(key)
        out = out + ''' ci.summary like "%{}%" or '''.format(key)
    return base_query + out[:-3] + " limit 10"

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

@app.route("/search")
def sesrch():
    return render_template("cvebykeyword.html")

@app.route("/styleGuide")
def styles():
    return render_template("styleGuide.html")

@app.route("/cveinfo")
def cveinfo():
    try:
        if request.args['cveid']:
            Session = scoped_session(sessionmaker(bind=engine))
            s = Session()
            try:
                # ooooo scaryy! FIXME: sanitize/escape user input!!!
                query = '''select cve_id, summary, access_vector, access_complexity, pub_date from cveitems where cve_id="{}";'''.format(request.args['cveid'])
                result = s.execute(query)
                print("Query Successful.")
                return render_template("cveinfo.html", result = result)
            except:
                print("Query Failed.")
                return render_template("404.html")
    except:
        return redirect(url_for('vendors'))


@app.route("/vulnerable-products", methods=["GET"])
def vuln_prod():
    try:
        if request.args['vendor']:
            Session = scoped_session(sessionmaker(bind=engine))
            s = Session()
            try:
                # ooooo scaryy! FIXME: sanitize/escape user input!!!
                query = '''select product, cve_id from `cve-vendors-products` as cvp, `cve-products` as cp where cvp.vendor = "{}" and cvp.product = cp.vulnerable_product'''.format(request.args['vendor'])
                result = s.execute(query)
                print("Query Successful.")
                return render_template("vendorsVulns.html", result = result)
            except:
                print("Query Failed.")
                return render_template("404.html")
    except:
        return redirect(url_for('vendors'))




@app.route("/vendors")
def vendors():
    Session = scoped_session(sessionmaker(bind=engine))
    s = Session()
    try:
        # ooooo scaryyy! FIXME: sanitize/escape user input!!!
        query = '''select cvp.vendor, count(ci.cve_id)
from cveitems as ci, `cve-products` as cp, `cve-vendors-products` as cvp
where ci.cve_id = cp.cve_id and cp.vulnerable_product = cvp.product
group by cvp.vendor
ORDER BY COUNT(ci.cve_id) DESC;'''
        result = s.execute(query)
        print("Query Successful.")
    except:
        print("Query Failed.")

    return render_template("vendorStats.html", result = result)

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
                # iterate through results
                for item in result:
                    print(item[0])
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


@app.route("/api/v1/search", methods=["GET", "POST"])
def search_endpoint():
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
                # iterate through results
                for item in result:
                    out = out + str(item)[1:-1] + ","
                print("Query Successful.")
                return "[" + out + "]"

            except:
                print("Query Failed.")
                return "Invalid SQL Statement or SQL error."
        else:
            return "No Query."

    else:
        return ">:("



if __name__ == '__main__':
    Flask.run(app, port="7777", debug=True)
    test = ["google" , "firefox", "safari"]
    print(xor(test))
