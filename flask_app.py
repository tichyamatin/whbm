import re,os,uuid
from pyvis.network import Network
from flask import Flask, render_template, request, url_for, redirect, session
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

def bmfilterprivate(testinput):
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

    net.save_graph('./templates/'+str(session['whbm_session'])+'.html')
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
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_HTTPONLY"] = False  # only for test

@app.route('/templates/<filename>')
def bmtest(filename):
    if not session.get("whbm_session"):
        filename = 'test.html'
        return render_template(filename)
    if session.get("whbm_session"):
        print('Session deteced')
        filename = '/templates/' + session.get("whbm_session") +'.html'
        #print(str(filename))
        templ = session.get("whbm_session")+'.html'
        return render_template(templ,filename=filename)


@app.route('/templates/<filename>')
def bmtestprivate(filename):
    print('enteredd send from')
    return send_from_directory('templates', filename)


'''
@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('template.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
'''

@app.route('/')
def bmupload():
    if not session.get("whbm_session"):
        print('No session cookie')
        session['whbm_session'] = '123'
    else:
        print(session['whbm_session'])

    return render_template('bmuploadpriv.html')

@app.route('/', methods=['POST'])
def bmuploadpost():
    testinput = request.form['textbox']
    bmfilterprivate(testinput)
    return render_template('bmuploadpriv.html')

if __name__ == '__main__':


    Session(app)

    app.run(debug=False)