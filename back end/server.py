import os
import json
import time
import queue
from flask import Flask, request, render_template, current_app, jsonify
from hole import *
from flask_cors import CORS
from apscheduler . schedulers .background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
cur_dir = os.path.dirname(__file__)
CORS(app, support_credentials=True)
hot_new_index_update()
hot_posts = select_hot_post()
user_client = {}
listen_people = queue.Queue()
tell_people = queue.Queue()
listen_man_people = queue.Queue()
tell_man_people = queue.Queue()
listen_woman_people = queue.Queue()
tell_woman_people = queue.Queue()


def update_hot_posts():
    hot_new_index_update()
    hot_posts = select_hot_post()

def hot_posts_get(post_index:int):
    ret = []
    if post_index>=len(hot_posts):
        return False
    else:
        right = post_index+10
        if right>len(hot_posts):
            right = len(hot_posts)
        for i in range(post_index,right):
            ret.append(hot_posts[i])
        return {"next_post_index":right,"ret":ret}

@app.route('/', methods=['GET'])
def start():
    return render_template('try.html')

@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('user')
    password = request.args.get('passwd')
    #res = {'status':True, 'name':'guodeyang'} #测试通信
    res = log_in_check(user, password) #测试数据库
    return jsonify(res)

@app.route('/register', methods=['GET'])
def register():
    user = request.args.get('user')
    password = request.args.get('passwd')
    name = request.args.get('name')
    #res = {'status':True} #测试通信
    res = log_up_check(user, name, password) #测试数据库
    return jsonify(res)

@app.route('/uptopic',methods=['POST'])
def up_topic():
    topic = request.get_json()
    #res = {'name': topic['n'], 'title': topic['t'], 'content': topic['c']} #测试通信
    res = post_in_db(topic['n'],topic['t'],topic['c'], topic['l'],topic['uname']) #测试数据库
    return jsonify(res)

@app.route('/gettopics',methods=['POST'])
def get_topics():
    topics = request.get_json()
    #res = [{'number': 1, 'title': 'azhe', 'content': 'azhe'},{'number': 2, 'title': 'zmx', 'content': 'zmx'}] #测试通信
    res = post_get(topics['n'], int(topics['w'])) #测试数据库
    return jsonify(res)

@app.route('/gettopic',methods=['POST'])
def get_topic():
    topic = request.get_json()
    #res = {'number': 1, 'data': '20200906', 'title': 'azhe', 'content': 'zmxssb', 'user': 'zmx', comment:['zhangmuxin', 'zmx']} #测试通信
    res = real_post_get(topic['nu'], topic['na']) #测试数据库
    return jsonify(res)

@app.route('/upcomment',methods=['POST'])
def up_comment():
    comment = request.get_json()
    res = comment_into_db(comment['c'], comment['na'], comment['nb'],comment['uname']) #测试数据库
    return jsonify(res)

@app.route('/askchat',methods=['POST'])
def ask_chat():
    newchat = request.get_json()
    res = have_unread_message(newchat['n']) #测试数据库
    return jsonify(res)

@app.route('/getchat',methods=['POST'])
def get_chat():
    chats = request.get_json()
    res = get_last_message(chats['n']) #测试数据库
    return jsonify(res)

@app.route('/lookchat',methods=['POST'])
def look_chat():
    lookedchat = request.get_json()
    res = get_ten_message(lookedchat['n'],lookedchat['w'],lookedchat['c'],int(lookedchat['wa'])) #测试数据库
    return jsonify(res)

@app.route('/chat',methods=['POST'])
def chat():
    ch = request.get_json()
    res = send_message(ch['n'],ch['w'],ch['c']) #测试数据库
    return jsonify(res)

@app.route('/getinfo',methods=['POST'])
def get_info():
    ginfo = request.get_json()
    res = get_user_information(ginfo['n']) #测试数据库
    return jsonify(res)

@app.route('/reinfo',methods=['POST'])
def re_info():
    rinfo = request.get_json()
    res = alter_user_information(rinfo['n'], rinfo['nn'], rinfo['s'], rinfo['i']) #测试数据库
    return jsonify(res)

@app.route('/starpost',methods=['POST'])
def star_post():
    st = request.get_json()
    res = like_post(st['n'], st['p'])#测试数据库
    return jsonify(res)

@app.route('/ustarpost',methods=['POST'])
def ustar_post():
    ust = request.get_json()
    res = dislike_post(ust['n'], ust['p'])#测试数据库
    return jsonify(res)

@app.route('/starcomment',methods=['POST'])
def star_comment():
    st = request.get_json()
    res = like_comment(st['n'], st['p'])#测试数据库
    return jsonify(res)

@app.route('/ustarcomment',methods=['POST'])
def ustar_comment():
    ust = request.get_json()
    res = dislike_comment(ust['n'], ust['p'])#测试数据库
    return jsonify(res)

@app.route('/delpost',methods=['POST'])
def del_post():
    de = request.get_json()
    res = delete_post(de['p'])#测试数据库
    return jsonify(res)

@app.route('/delcomment',methods=['POST'])
def del_comment():
    de = request.get_json()
    res = delete_comment(de['p'])#测试数据库
    return jsonify(res)

@app.route('/collectpost',methods=['POST'])
def collect_post():
    co = request.get_json()
    res = post_collect(co['n'], co['p'])#测试数据库
    return jsonify(res)

@app.route('/ucollectpost',methods=['POST'])
def ucollect_post():
    uco = request.get_json()
    res = post_remove_collect(uco['n'], uco['p'])#测试数据库
    return jsonify(res)

@app.route('/getuserpost',methods=['POST'])
def get_post():
    ge = request.get_json()
    res = get_user_posts(ge['n'])#测试数据库
    return jsonify(res)

@app.route('/getusecollect',methods=['POST'])
def get_collect():
    ge = request.get_json()
    res = get_collect_posts(ge['n'])#测试数据库
    return jsonify(res)

@app.route('/search', methods=['POST'])
def post_search():
    se = request.get_json()
    res = search_post(se['key_word'])#测试数据库
    return jsonify(res)

@app.route('/hottopic',methods=['POST'])
def hot_topic():
    req = request.get_json()
    board = req['l']
    if(board=='hot'):
        ret = hot_posts_get(int(req['n']))
    else:
        ret = post_get(req['n'],int(req['w']),req['l'])
    return jsonify(ret)

@app.route('/love',methods=['POST'])
def search_love():
    res = {'status':True,'data':None}
    ho = request.get_json()
    sex = search_sex(ho['name'])
    if ho['li_te'] == '1':
        if ho['way'] == '1':
            if sex == '男':
                while True:
                    if tell_woman_people.empty():
                        listen_man_people.put(ho['name'])
                        user_client[ho['name']] = queue.Queue()
                        try:
                            users = user_client[ho['name']].get()
                            if users:
                                res['data'] = users
                            else:
                                res['status'] = False
                        except queue.Empty:
                            res['status'] = False
                        del user_client[ho['name']]
                        break
                    else:
                        users = tell_woman_people.get()
                        if user_client.get(users, False):
                            user_client[users].put(ho['name'])
                            res['data'] = users
                            break
            else:
                while True:
                    if tell_man_people.empty():
                        listen_woman_people.put(ho['name'])
                        user_client[ho['name']] = queue.Queue()
                        try:
                            users = user_client[ho['name']].get()
                            if users:
                                res['data'] = users
                            else:
                                res['status'] = False
                        except queue.Empty:
                            res['status'] = False
                        del user_client[ho['name']]
                        break
                    else:
                        users = tell_man_people.get()
                        if user_client.get(users, False):
                            user_client[users].put(ho['name'])
                            res['data'] = users
                            break
        else:
            while True:
                if tell_people.empty():
                    listen_people.put(ho['name'])
                    user_client[ho['name']] = queue.Queue()
                    try:
                        users = user_client[ho['name']].get()
                        if users:
                            res['data'] = users
                        else:
                            res['status'] = False
                    except queue.Empty:
                        res['status'] = False
                    del user_client[ho['name']]
                    break
                else:
                    users = tell_people.get()
                    if user_client.get(users, False):
                        user_client[users].put(ho['name'])
                        res['data'] = users
                        break
    else:
        if ho['way'] == '1':
            if sex == '男':
                while True:
                    if listen_woman_people.empty():
                        tell_man_people.put(ho['name'])
                        user_client[ho['name']] = queue.Queue()
                        try:
                            users = user_client[ho['name']].get()
                            if users:
                                res['data'] = users
                            else:
                                res['status'] = False
                        except queue.Empty:
                            res['status'] = False
                        del user_client[ho['name']]
                        break
                    else:
                        users = listen_woman_people.get()
                        if user_client.get(users, False):
                            user_client[users].put(ho['name'])
                            res['data'] = users
                            break
            else:
                while True:
                    if listen_man_people.empty():
                        tell_woman_people.put(ho['name'])
                        user_client[ho['name']] = queue.Queue()
                        try:
                            users = user_client[ho['name']].get()
                            if users:
                                res['data'] = users
                            else:
                                res['status'] = False
                        except queue.Empty:
                            res['status'] = False
                        del user_client[ho['name']]
                        break
                    else:
                        users = listen_man_people.get()
                        if user_client.get(users, False):
                            user_client[users].put(ho['name'])
                            res['data'] = users
                            break
        else:
            while True:
                if listen_people.empty():
                    tell_people.put(ho['name'])
                    user_client[ho['name']] = queue.Queue()
                    try:
                        users = user_client[ho['name']].get()
                        if users:
                            res['data'] = users
                        else:
                            res['status'] = False
                    except queue.Empty:
                        res['status'] = False
                    del user_client[ho['name']]
                    break
                else:
                    users = listen_people.get()
                    if user_client.get(users, False):
                        user_client[users].put(ho['name'])
                        res['data'] = users
                        break
    return jsonify(res)

@app.route('/cancel',methods=['POST'])
def cancel():
    ho = request.get_json()
    if user_client.get(ho['name'], False):
        user_client[ho['name']].put(False)
    else:
        return jsonify(False)
    return jsonify(True)

@app.route('/unamechat',methods=['POST'])
def uname_chat():
    un = request.get_json()
    res = select_friend_anonymous(un['n'], un['w'])
    return jsonify(res)

@app.route('/report',methods=['POST'])
def report():
    rp = request.get_json()
    if rp['w']:
        res = post_report(rp['n'], rp['nu'], rp['r'])
    else:
        res = comment_report(rp['n'], rp['nu'],rp['r'])
    return jsonify(res)

@app.route('/unamechange',methods=['POST'])
def unamec_change():
    un = request.get_json()
    res = set_chat_anonymous(un['n'], un['w'])
    return jsonify(res)

@app.route('/getreports',methods=['POST'])
def getreports():
    req = request.get_json()
    ret = select_report()
    return jsonify(ret)

@app.route('/handlereport',methods=['POST'])
def handlereport():
    req = request.get_json()
    ret = handle_report(int(req['r']),req['w'],req['nu'],req['r_id'])
    return jsonify(ret)

if __name__ == "__main__":
    scheduler = BackgroundScheduler(timezone='MST')
    scheduler.add_job(update_hot_posts, 'interval', minutes=10)
    scheduler.start()
    app.run(host='0.0.0.0', port='8080', debug=False)
