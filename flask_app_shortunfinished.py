import re,os,uuid
from pyvis.network import Network
from flask import Flask, render_template, request, url_for, redirect



testinput='''
1/1^1,3,4
1/1^2,2
1/1^3
1/2^3
1/3^2
1/3^3
1/3^4
1/4^2,5
1/4^3
1/4^4
1/5^3
1/5^4
2/1^1
2/1^2
'''

def unique(list1):

    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list




def bmfilter(testinput):
    #>>>FILTERING OUTPUT
    testinput = testinput.replace('[','')
    testinput = testinput.replace(']','')
    testinput = testinput.replace('(','')
    testinput = testinput.replace(')','')
    testinput = testinput.replace('  ',' ')
    print('Filtered:')
    print(testinput)

    #print('Output:')
    #searchObj = re.search( r'(\d*\/\d*\^\w*)', testinput)
    #print(searchObj)
    searchObj = re.findall( r'(\d)\/(\d)\^(\w*)', testinput)
    searchObj2 = re.findall( r'(\d\/\d\^\w*)([,\d]*)', testinput)

    #print(searchObj)

    roots = []
    branch1 = []
    branch2 = []

    bmids = []
    bmlabels = []
    bmconnections = []

    for root in searchObj:
        roots.append(root[0])
        branch1.append(root[1])
        branch2.append(root[2])

    for r in unique(roots):
        #print('Tree: '+r)
        for item in searchObj:
            #print(searchObj)
            if item[0] == r:

                #ADD bmids
                bmids.append(r+'/'+item[1]+'^'+item[2])

                #ADD bmlabels
                bmlabels.append(r+'/'+item[1]+'^'+item[2])

                basenode = (r,item[1],item[2])

                distance_next = str(int(item[2])+1)

                #print('Basenode: '+str(basenode))

                #connecting nodes
                for branch in unique(branch1):
                    #branchup = int(branch)+1
                    if branch == item[1]:

                        connectnode = (r,branch,distance_next)

                        if connectnode in searchObj:
                            #print('Connections: ')
                            #print(str(basenode)+' > '+str(connectnode))
                            #print('%s/%s^%s' % (r,item[1],item[2]))
                            #print('%s/%s^%s' % (r,item[1],distance_next))

                            #ADD CONNECTIONS
                            bmfrom = r+'/'+item[1]+'^'+item[2]
                            bmto = r+'/'+item[1]+'^'+distance_next

                            bm_con = (bmfrom,bmto)
                            bmconnections.append(bm_con)

    if searchObj2:
        #print(searchObj2)
        for i in searchObj2:
            #print(i)
            if len(i[1]) > 0:
                searchObj3 = re.findall( r'\d*', i[1])
                for b in searchObj3:
                    if b != '':
                        print(i[0])
                        print(b)

>>>>>>>>>>>>>>>>>>      TU PODJAC DALEJ
                        finder = re.findall( r'(\d)\/(\d)\^(\w*)', testinput)


                        if searchObj =

                        #bmfrom = r+'/'+item[1]+'^'+item[2]
                        #bmto = r+'/'+item[1]+'^'+distance_next

                        #bm_con = (bmfrom,bmto)
                        #bmconnections.append(bm_con)



    #print(bmconnections)

    '''
    #connecting branches
    for branch in unique(branch1):
        #branchup = int(branch)+1
        if branch > item[1]:

            connectnode = (r,branch,distance_next)

            if connectnode in searchObj:
                print('Branch Connections: ')
                print(str(basenode)+' > '+str(connectnode))
    '''


    #>>> CREATING LIST AND POPULATIN WITH FILTERED DATA

    '''
    for bm in searchObj:
        bmids.append(bm[0])
        bmids.append(bm[2])

        bmlabels.append(str('('+bm[0] +') '+ bm[1]))
        bmlabels.append(str('('+bm[2] +') '+ bm[3]))

        bm_con = (bm[0],bm[2])
        bmconnections.append(bm_con)
    '''

    #print(bmids)
    #print(type(bmids))

    #>>> GRAPH CREATION
    net = Network(
        notebook=True,
        cdn_resources="remote",
        bgcolor="#222222",
        font_color="white",
        height="750px",
        width="100%",
    )

    net.add_nodes(bmids,label=bmlabels)
    net.add_edges(bmconnections)
    net.repulsion(node_distance=80, spring_length=40)

    id = uuid.uuid1()
    idnode = str(id.node)

    net.save_graph('./templates/test.html')


bmfilter(testinput)


'''
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def bmform():
    return render_template('bmupload.html')

@app.route('/', methods=['POST'])
def bmform_post():
    #os.remove('./templates/test.html')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!testinput = request.form['textbox']
    bmfilter(testinput)
    return render_template('test.html')

if __name__ == '__main__':

    app.run(debug=False)
'''
