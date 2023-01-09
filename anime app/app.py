from flask import Flask , render_template , request ,jsonify
from flask_pymongo import *
from bson.json_util import dumps 
from flask_cors import CORS,cross_origin


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://abdobel:bigSO9pKTKCqXwDv@cabdobel.qaooxhy.mongodb.net/animes"
mongo = PyMongo(app)

CORS(app, support_credentials=True)



anime = mongo.db.myanime.find()

# ---------------- api page render -------------------
@app.route('/api/anime', methods=['POST', 'GET','OPTIONS'])
@cross_origin(supports_credentials=True)
def index():
    x = dumps(anime , ensure_ascii = False)
    if(request.method=='POST'):
        some_json=request.get_json()
        return jsonify({"key":some_json})
    else:
        return x



# ------------------------ home page render ----------------------
@app.route('/')
def home_page():
    anime_data= []
    episode_new = mongo.db.newepisode.find()
    for i in episode_new:
        anime_data.append(i)
    anime_data.reverse()
    new_anime = []
    for ii in range(24):
        anime = mongo.db.myanime.find_one({"anime_titel":anime_data[ii]["anime_titel"]})
        if anime != None:
            epis = anime_data[ii]["episode_number"]
            epis_num = epis.split()
            new_anime.append({"anime":anime,"episode_number":int(epis_num[1])})
    anime_last = mongo.db.myanime.find()
    anime_last_list = []
    for item in anime_last:
        anime_last_list.append(item)
    anime_last_list.reverse()
    anime_last_add = []
    for elm in range(10):
        anime_last_add.append(anime_last_list[elm])
    
    return render_template('home_page.html',episode_new = new_anime ,anime_last_add = anime_last_add)

#---------------------- anime seson render --------------
@app.route('/anime-seson')
def anime_seson():
    showing_now = mongo.db.myanime.find()
    anime_showing_now = []
    print(showing_now[0])
    for ii in showing_now:
        if ii["anime_info"][2] == "حالة الأنمي: يعرض الان":
            anime_showing_now.append(ii)
    return render_template('anime_seson.html' ,anime_showing_now = anime_showing_now)

#---------------------- anime move render --------------
@app.route('/anime-movei')
def anime_movei():
    movei = mongo.db.myanime.find()
    anime_movei = []
    for ii in movei:
        if ii["anime_info"][0] == "النوع: Movie":
            anime_movei.append(ii)
    return render_template('movei.html' ,anime_movei = anime_movei)


#-------------------- list page render --------------------
@app.route('/list-page')
def list_page():
    anime_ls1 = []
    for i in range(30):
        try:
            anime_ls1.append(anime[i])
        except:
            break
    return render_template('list_page.html' , info=anime_ls1 ,next_id=1)

    

@app.route('/list-page/<string:id>/')
def list_page_id(id): 
    anime_ls = []
    try:
        id_number = int(id)
        i = (id_number-1) * 30
        cont = id_number * 30
        while i < cont:
            try:
                anime_ls.append(anime[i])
            except:
                break
            i = i + 1
        return render_template('list_page.html' , info=anime_ls , next_id=id_number)
    except:
        return '<h1>page not found </h1>'


#---------------------- anime info page ------------
@app.route('/anime/<string:id>/')
def anime_info(id):
    name_ =  id 
    anime_info_data = mongo.db.myanime.find_one({"anime_titel":name_})
    return render_template('info_page.html',info_data = anime_info_data)


def Convert(string):
    list1 = []
    list1[:0] = string
    return list1


@app.route('/woch-page/<string:id>/')
def woch_page(id):
    try:
        titel = ''
        num = ''
        i = len(id) - 1
        while i > 0 :
            if id[i] == "-":
                l = i
                break
            i = i - 1
        for ii in range(l):
            titel += id[ii]
        n = l +1
        while n < len(id):
            num += id[n]
            n = n+1

        anime_info_data = mongo.db.myanime.find_one({"anime_titel":titel})
        return render_template('woch.html',anime_info = anime_info_data ,epsode_num = int(num))
    except:
        return '<h2>page not found</h1>'











if __name__ =='__main__':
    app.run(debug=True)