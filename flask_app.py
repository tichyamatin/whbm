import re, os, uuid, time, base64, requests, json
from pyvis.network import Network
from flask import Flask, render_template, request, url_for, redirect, session
from bs4 import BeautifulSoup
from flask_session import Session


#redirecturi = 'http%3A%2F%2Flocalhost%3A5000%2Fcallback%2F'   #TEST http://localhost:5000/callback/
#redirecturi = 'https%3A%2F%2Fwhbm.pythonanywhere.com%2Fcallback%2F'     #PROD https://whbm.pythonanywhere.com/callback/

with open('./config/whbm.config') as f:
    config = json.load(f)
    redirecturi = config['redirecturi']
    clientid = config['clientid']
    secretkey = config['secretkey']
    responsetyp = config['responsetyp']
    scope = config['scope']
    state = config['state']



authredirurl = 'https://login.eveonline.com/oauth/authorize?response_type=' + responsetyp + '&redirect_uri=' + redirecturi + '&client_id=' + clientid + '&scope=' + scope + '&state=' + state

clientsecretpair = base64.b64encode(bytes(clientid + ':' + secretkey, 'ascii'))
clientsecretpair = str(clientsecretpair, 'utf-8')
clientsecretpair = 'Basic ' + clientsecretpair

def timestamp():
    return round(time.time() * 1000)

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
    clearfile('./templates/test.html')

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
    clearfile('./templates/'+str(session['whbm_session'])+'.html')

def clearfile(file_path):
    htmlfile = file_path

    f = open(htmlfile, "r")
    filecontent1 = f.read()
    f.close()

    soup = BeautifulSoup(filecontent1, "html.parser")
    filecontentfixed = str(soup.prettify())

    filecontentfixed = re.sub(r'\s*<center>\n\s*<h1>\n\s*<\/h1>\n\s*<\/center>', '', filecontentfixed)
    filecontentfixed = re.sub(r'border:\s1px\ssolid\slightgray', 'border: 0px solid lightgray', filecontentfixed)
    filecontentfixed = re.sub(r'<\/style>\n\s*<\/head>\n\s*<body>\n\s*<div\sclass\=\"card\"\s*style\=\"width:\s100%\">', ' \n body {background-color: #0C011D;}</style></head><body><div class=\"card\" style=\"border:none\">', filecontentfixed)


    f = open(htmlfile, "w")
    f.write(filecontentfixed)
    f.close()

    '''
    with open(htmlfile) as f:
        lines = [i for i in f.readlines() if i and i != '\n']
    '''
    '''
    with open(htmlfile, 'w') as f:
        f.writelines(lines)
    '''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A&*SD^*(A&SD^A*&SD^*A&SD^*'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"

privategraph = True

@app.route('/templates/<filename>')
def bmtest(filename):
    global privategraph

    if not privategraph:
        filename = '/templates/test.html'
        templ = 'test.html'
        return render_template(templ,filename=filename)

    if privategraph:
        filename = '/templates/' + str(session.get("whbm_session")) +'.html'
        try:
            templ = str(session.get("whbm_session"))+'.html'
            return render_template(templ, filename=filename)
        except:
            return render_template('blank.html', filename=filename)

@app.route('/templates/<filename>')
def bmtestprivate(filename):
    return send_from_directory('templates', filename)

@app.route('/')
def bmupload():
    global privategraph
    if not session.get("whbm_session"):
        print('No session cookie')
        return redirect(url_for('eveoauth'))
    else:
        print(session['whbm_session'])

        if request.args.get('priv') == 'PUBLIC':
            print('changing to false')
            privategraph = False
        if request.args.get('priv') == 'PRIVATE':
            privategraph = True
            print('changing to true')

        if privategraph:
            return render_template('bmuploadpriv.html', privategraph=privategraph)
        else:
            return render_template('bmuploadpriv.html', privategraph=privategraph)


@app.route('/', methods=['POST'])
def bmuploadpost():
    global privategraph

    testinput = request.form['textbox']

    if privategraph:
        bmfilterprivate(testinput)
        return render_template('bmuploadpriv.html', privategraph=privategraph)
    else:
        bmfilter(testinput)
        return render_template('bmuploadpriv.html', privategraph=privategraph)

@app.route('/oauth/')
def eveoauth():
    return redirect(authredirurl, code=302)

@app.route('/callback/')
def callback():
    #1 - Get code and state from callback return
    code = request.args.get('code')
    state = request.args.get('state')

    #2 - Get JWT Auth Token
    postpayload = {"grant_type":"authorization_code", "code":code}
    x = requests.post('https://login.eveonline.com/oauth/token', json=postpayload, headers={"Content-Type": "application/json", "Authorization": clientsecretpair})
    token = x.json()
    authtoken = str(token["access_token"])

    #3 - Authenticate
    z = requests.get('https://login.eveonline.com/oauth/verify', headers={"Content-Type": "application/json", "Authorization": "Bearer " + authtoken})
    resp = z.json()

    #4 - Send Authenticated request
    y = requests.get('https://esi.evetech.net/latest/characters/'+str(resp["CharacterID"]), headers={"Content-Type": "application/json", "Authorization": "Bearer " + authtoken})
    resp = y.json()
    corpid = resp["corporation_id"]

    if corpid == 98719586:
        session['whbm_session'] = timestamp()
        return redirect(url_for('bmupload'))

    else:
        return 'You are not a member.'

if __name__ == '__main__':

    Session(app)
    app.run(debug=True)