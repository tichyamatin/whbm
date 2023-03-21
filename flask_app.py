import re,os,uuid
from pyvis.network import Network
from flask import Flask, render_template, request, url_for, redirect, session
import requests
from bs4 import BeautifulSoup
from flask_session import Session

def bmfilter(testinput):
    #>>>FILTERING INPUT
    testinput = testinput.replace('[','')
    testinput = testinput.replace(']','')
    testinput = testinput.replace('(','')
    testinput = testinput.replace(')','')
    testinput = testinput.replace('  ',' ')
    print(len(testinput))

    searchObj = re.findall( r'\w\-\d\s(.*?)\s*(&gt;|&lt;|<|>)\s*(\w*)\s*(Coordinate|(.*?)Coordinate)', testinput)

    #>>> CREATING LIST AND POPULATIN WITH FILTERED DATA
    bmids = []
    bmlabels = []
    bmconnections = []

    for bm in searchObj:
        bmids.append(bm[0])
        bmids.append(bm[2])

        bmlabels.append(str(bm[0]))
        bmlabels.append(str(bm[2]))

        bm_con = (bm[0],bm[2])
        bmconnections.append(bm_con)

    print(bmids)
    print(type(bmids))

    #>>> GRAPH CREATION
    net = Network(
        notebook=True,
        cdn_resources="remote",
        bgcolor="#0C011D",
        font_color="#00B4FF",
        height="750px",
        width="100%",
    )

    net.add_nodes(bmids,label=bmlabels)
    net.add_edges(bmconnections)
    net.repulsion(node_distance=80, spring_length=40)

    id = uuid.uuid1()
    idnode = str(id.node)

    net.save_graph('./templates/test.html')
    #clearfile()


def clearfile():

    htmlfile = "./templates/test.html"

    f = open(htmlfile, "r")
    filecontent1 = f.read()
    f.close()

    soup = BeautifulSoup(filecontent1, "html.parser")
    filecontentfixed = str(soup.prettify())
    print(filecontentfixed)

    f = open(htmlfile, "w")
    f.write(filecontentfixed)
    f.close()

    with open(htmlfile) as f:
        lines = [i for i in f.readlines() if i and i != '\n']

    with open(htmlfile, 'w') as f:
        f.writelines(lines)


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/templates/test.html')
def bmtest():
    return render_template('test.html')

@app.route('/')
def bmupload():
    return render_template('bmupload.html')

@app.route('/', methods=['POST'])
def bmuploadpost():
    testinput = request.form['textbox']
    bmfilter(testinput)
    return render_template('bmupload.html')

if __name__ == '__main__':

    app.run(debug=False)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)