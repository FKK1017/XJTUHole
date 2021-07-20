# coding=utf-8
import mysql.connector,sys,traceback,hashlib,time

mysql_user = "kkuan"
mysql_password = "enderii2"
database_name = "XJTUHole"

def log_in_check(account:str,password:str):
    if (not account) or (not password):
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    h1 = hashlib.md5()
    h1.update(password.encode(encoding='utf-8'))
    password = h1.hexdigest()
    sql = "select user_name from user_information where user_account='"+account+"' and user_password='"+password+"'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        return {'name':None,'status':False}
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if not result:
        return {'name':None,'status':False}
    else:
        return {'name':result[0][0],'status':True}

def log_up_check(account:str,name:str,password:str):    #检测账号和用户名是否已经存在，存在则返回标志码，不存在则加入数据库，返回True,数据库操作出错则返回False
    if (not account) or (not name) or (not password):
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    sql = "select user_name from user_information where user_account='" + account + "'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if not result:
        sql = "select user_name from user_information where user_name='" + name + "'"
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        result = cursor.fetchall()
        if not result:
            h1 = hashlib.md5()
            h1.update(password.encode(encoding='utf-8'))
            password = h1.hexdigest()
            sql = "insert into user_information(user_account,user_name,user_password,register_date) values('"+account+"','"+name+"','"+password+"',date_format(now(),'%y-%m-%d'))"
            try:
                cursor.execute(sql)
                db.commit()
                db.close()
                return True
            except:
                traceback.print_exc()
                db.close()
                return False
        else:
            db.close()
            return False        #用户名已经存在
    else:
        db.close()
        if result[0][0]!=name:
            return False        #账号已经存在
        else:
            return False        #用户名和账号都存在了

def get_user_information(user_name:str): #获取个人信息
    if(not user_name):
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    sql = "select sex,register_date,post_count,introduction from user_information where user_name='"+user_name+"'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    results = cursor.fetchall()
    if not results:
        db.close()
        traceback.print_exc()
        return False
    else:
        db.close()
        if results[0][0]==None:
            sex = '保密'
        else:
            sex = results[0][0]
        register_date = (results[0][1]).strftime('%Y-%m-%d')
        post_count = str(results[0][2])
        introduction = results[0][3]
        if introduction==None:
            introduction="这家伙很懒，什么都没有留下~"
        return {'sex':sex,'register_date':register_date,'post_count':post_count,'introduction':introduction}

def alter_user_information(old_user_name:str,new_user_name:str,sex:str,introduction:str):
    if(not new_user_name) or (not sex):
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name='" + old_user_name + "'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        traceback.print_exc()
        return False
    else:
        user_id = result[0][0]
    if sex=='保密':
        sql = "update user_information set user_name='"+new_user_name+"',sex=NULL,introduction='"+introduction+"' where user_id="+str(user_id)
    else:
        sql = "update user_information set user_name='" + new_user_name + "',sex='"+sex+"',introduction='" + introduction + "' where user_id=" + str(user_id)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.close()
        traceback.print_exc()
        return False

def post_in_db(user_name:str,title:str,content:str,board:str,*args):
    if (not user_name) or (not title) or (not content):
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name='"+user_name+"'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        traceback.print_exc()
        return False
    else:
        author_id = result[0][0]
        if args:
            is_an = str(int(args[0]))
            sql1 = "insert into post(title,content,browse_count,post_time,author_id,board,is_anonymous) values('%s','%s',0,now(),%s,'%s',%s)" % (
            title, content, str(author_id), board, is_an)
        else:
            sql1 = "insert into post(title,content,browse_count,post_time,author_id,board) values('%s','%s',0,now(),%s,'%s')" % (
                title, content, str(author_id), board)
        sql2 = "update user_information set post_count=post_count+1 where user_id="+str(author_id)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return True
        except:
            db.close()
            print(traceback.print_exc())
            return False

def post_get(post_id:str,way:int,*args): #获取帖子列表
    if (not post_id):
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    sql = ""
    if way==1:
        if args:
            sql = "select post_id,title,content,comment_count,like_count,collect_count,board from post where is_delete = 0 and board = '%s' order by post_id desc limit 0,10" % (args[0])
        else:
            sql = "select post_id,title,content,comment_count,like_count,collect_count,board from post where is_delete = 0 order by post_id desc limit 0,10"      #最新十条
    elif way==0:
        if args:
            sql = "(select post_id,title,content,comment_count,like_count,collect_count,board from post where is_delete = 0 and board = '%s' and post_id>%s order by post_id limit 0,10) order by post_id desc" % (args[0],post_id)
        else:
            sql = "(select post_id,title,content,comment_count,like_count,collect_count,board from post where is_delete = 0 and post_id>"+post_id+" order by post_id limit 0,10) order by post_id desc"  #后面十条
    elif way==2:
        if args:
            sql = "select post_id,title,content,comment_count,like_count,collect_count,board from post where is_delete = 0 and board = '%s' and post_id<%s order by post_id desc limit 0,10" % (args[0],post_id)  # 前面十条
        else:
            sql = "select post_id,title,content,comment_count,like_count,collect_count,board from post where is_delete = 0 and post_id<"+post_id+" order by post_id desc limit 0,10"               #前面十条
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        traceback.print_exc()
        db.close()
        return False
    db.close()
    ret = []
    for result in results:
        if len(result[2]) > 100:
            content = (result[2])[0:100]
        else:
            content = result[2]
        if len(result[1]) > 15:
            title = (result[1])[0:15]
        else:
            title = result[1]
        comment_count = str(result[3])
        like_count = str(result[4])
        collect_count = str(result[5])
        board = str(result[6])
        ret.append({'post_id': result[0], 'title': title, 'content': content, 'comment_count': comment_count, 'like_count': like_count,"collect_count":collect_count,"board":board})
    return ret

def real_post_get(post_id:str,user_name:str): #获取帖子所有内容
    if not post_id:
        return False
    db = mysql.connector.connect(
        host = "localhost",
        user = mysql_user,
        passwd = mysql_password,
        database = database_name
    )
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql = "select title,content,browse_count,post_time,author_id,have_picture,board,like_count,collect_count,is_anonymous from post where is_delete = 0 and post_id = "+post_id
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    results = cursor.fetchall()
    if not results:
        db.close()
        return False
    title = results[0][0]
    content = results[0][1]
    browse_count = results[0][2]
    post_time = (results[0][3]).strftime('%Y-%m-%d %H:%M')
    author_id = results[0][4]
    have_picture = results[0][5]
    board = results[0][6]
    like_count = results[0][7]
    collect_count = results[0][8]
    is_anonymous = bool(results[0][9])
    sql = "update post set browse_count=browse_count+1 where post_id="+post_id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.close()
        traceback.print_exc()
        return False
    sql = "select user_name from user_information where user_id = "+str(author_id)
    try:
        cursor.execute(sql)
    except:
        traceback.print_exc()
        db.close()
        return False
    results = cursor.fetchall()
    author_name = results[0][0]
    sql = "select comment_id from comment where is_delete = 0 and post_id = "+post_id+" order by comment_id"
    try:
        cursor.execute(sql)
    except:
        db.close()
        print(traceback.print_exc())
        return False
    results = cursor.fetchall()
    comment_list=[]
    for result in results:
        comment_list.append(comment_get(str(result[0]),user_id))
    ret = {'title':title,'content':content,'browse_count':browse_count,'post_time':post_time,'author_name':author_name,'have_picture':have_picture,'comment':comment_list,"board":board,"like_count":like_count,"collect_count":collect_count,"is_anonymous":is_anonymous}
    try:
        sql = "select is_like from post_like where post_id=%s and user_id=%s" % (post_id,user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result or result[0][0]==0:
            like = False
        else:
            like = True
        sql = "select dislike from post_dislike where post_id=%s and user_id=%s" % (post_id, user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result or result[0][0] == 0:
            dislike = False
        else:
            dislike = True
        sql = "select * from post_collect where post_id=%s and user_id=%s" % (post_id, user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            collect = False
        else:
            collect = True
        ret["like"] = like
        ret["dislike"] = dislike
        ret["collect"] = collect
    except:
        db.close()
        return False
    db.close()
    return ret

def comment_into_db(content:str,author_name:str,post_id:str,*args): #评论加载到数据库
    if (not content) or (not author_name) or (not post_id):
        return False
    db = mysql.connector.connect(
        host = "localhost",
        user = mysql_user,
        passwd = mysql_password,
        database = database_name
    )
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '"+author_name+"'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    author_id = result[0][0]
    if args:
        is_an = str(int(args[0]))
        sql1 = "insert into comment(content,comment_time,author_id,post_id,is_anonymous) values('"+content+"',now(),"+str(author_id)+","+post_id+","+is_an+")"
    else:
        sql1 = "insert into comment(content,comment_time,author_id,post_id) values('"+content+"',now(),"+str(author_id)+","+post_id+")"
    sql2 = "update post set comment_count=comment_count+1 where post_id="+post_id
    try:
        cursor.execute(sql1)
        sql = "select LAST_INSERT_ID()"
        cursor.execute(sql)
        comment_id = str((cursor.fetchall())[0][0])
        cursor.execute(sql2)
        db.commit()
        db.close()
        return {"comment_id":comment_id}
    except:
        db.close()
        traceback.print_exc()
        return False

def comment_get(comment_id:str,user_id:str): #获取评论内容
    if not comment_id:
        return False
    db = mysql.connector.connect(
        host = "localhost",
        user = mysql_user,
        passwd = mysql_password,
        database = database_name
    )
    cursor = db.cursor()
    sql="select content,comment_time,author_id,is_anonymous from comment where comment_id="+comment_id
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    results = cursor.fetchall()
    if not results:
        db.close()
        return False
    content = results[0][0]
    comment_time = (results[0][1]).strftime('%Y-%m-%d %H:%M')
    author_id = results[0][2]
    is_anonymous = bool(results[0][3])
    sql = "select user_name from user_information where user_id = "+str(author_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        print(traceback.print_exc())
        return False
    results = cursor.fetchall()
    author_name = results[0][0]
    ret = {'comment_id':comment_id,'content':content,'comment_time':comment_time,'author_name':author_name,'is_anonymous':is_anonymous}    #返回评论内容，评论时间，评论者用户名
    try:
        sql = "select is_like from comment_like where comment_id=%s and user_id=%s" % (comment_id,user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result or result[0][0]==0:
            like = False
        else:
            like = True
        sql = "select dislike from comment_dislike where comment_id=%s and user_id=%s" % (comment_id, user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result or result[0][0] == 0:
            dislike = False
        else:
            dislike = True
        ret["like"] = like
        ret["dislike"] = dislike
    except:
        traceback.print_exc()
        db.close()
        return False
    db.close()
    return ret

def have_unread_message(user_name:str):
    if not user_name:
        return False
    db = mysql.connector.connect(
        host = "localhost",
        user = mysql_user,
        passwd = mysql_password,
        database = database_name
    )
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '" + user_name + "'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        return False
    user_id = result[0][0]
    sql = "select count(*) from private_message where receiver_id = "+str(user_id)+" and is_read = 0"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    results = cursor.fetchall()
    message_count = results[0][0]
    db.close()
    if message_count>0:
        return {"have_message":True,"message_count":message_count}
    else:
        return {"have_message":False,"message_count":0}

def get_last_message(user_name:str):
    if not user_name:
        return False
    db = mysql.connector.connect(
        host = "localhost",
        user = mysql_user,
        passwd = mysql_password,
        database = database_name
    )
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '" + user_name + "'"
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    user_id = result[0][0]
    sql = "select friend_id from friend where user_id = "+str(user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    results = cursor.fetchall()
    friend_id_list = []
    ret = []
    for result in results:
        friend_id_list.append(result[0])
    print(friend_id_list)
    for friend_id in friend_id_list:
        sql = "select user_name from user_information where user_id= "+str(friend_id)
        try:cursor.execute(sql)
        except:
            db.close()
            traceback.print_exc()
            return False
        result = cursor.fetchall()
        ret.append({'user_name':result[0][0]})
    for i in range(len(friend_id_list)):
        sql = "select content,time from private_message where (sender_id = "+ str(user_id)+" and receiver_id = "+str(friend_id_list[i])+") or (sender_id = "+str(friend_id_list[i])+" and receiver_id = "+str(user_id)+") ORDER BY message_id DESC LIMIT 0,1"
        try:
            cursor.execute(sql)
        except:
            db.close()
            traceback.print_exc()
            return False
        result = cursor.fetchall()
        if len(result)>0:
            ret[i]['content'] = result[0][0]
            ret[i]['time'] = str(result[0][1])
        sql = "select message_id from private_message where sender_id = "+str(friend_id_list[i])+" and receiver_id = "+str(user_id)+" and is_read = 0"
        try:cursor.execute(sql)
        except:
            db.close()
            traceback.print_exc()
            return False
        result = cursor.fetchall()
        if not result:
            ret[i]['have_message'] = False
            ret[i]['message_count'] = 0
        else:
            ret[i]['have_message'] = True
            ret[i]['message_count'] = len(result)
    ret=sorted(ret,key=lambda x:x['time'],reverse=True)
    db.close()
    return ret

def get_ten_message(user_name:str,friend_name:str,message_id:str,way:int):
    if (not user_name) or (not friend_name) or (not message_id):
        return False
    db = mysql.connector.connect(
        host = "localhost",
        user = mysql_user,
        passwd = mysql_password,
        database = database_name
    )
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '" + user_name + "'"
    try:cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        return False
    user_id = result[0][0]
    sql = "select user_id from user_information where user_name = '" + friend_name + "'"
    try:cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        return False
    friend_id = result[0][0]
    sql = ""
    if way==1:
        sql = "select message_id,sender_id,content,time from private_message where (sender_id = "+ str(user_id)+" and receiver_id = "+str(friend_id)+") or (sender_id = "+str(friend_id)+" and receiver_id = "+str(user_id)+") order by message_id desc limit 0,10"      #最新十条
    #elif way==0:
    #    sql = "(select message_id,sender_id,content,time from private_message where message_id>"+message_id+"and ((sender_id = "+ str(user_id)+" and receiver_id = "+str(friend_id)+") or (sender_id = "+str(friend_id)+" and receiver_id = "+str(user_id)+")) order by message_id limit 0,10) order by message_id desc"  #后面十条
    elif way==0:
        sql = "select message_id,sender_id,content,time from private_message where message_id<"+message_id+" and ((sender_id = "+ str(user_id)+" and receiver_id = "+str(friend_id)+") or (sender_id = "+str(friend_id)+" and receiver_id = "+str(user_id)+")) order by message_id desc limit 0,10"               #前面十条
    elif way==2:
        sql = "select message_id,sender_id,content,time from private_message where sender_id="+str(friend_id)+" and receiver_id="+str(user_id)+" and is_read=0 order by message_id desc"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print(traceback.print_exc())
        db.close()
        return False
    ret = []
    if not result:
        db.close()
        return ret
    for result in results:
        cursor = db.cursor()
        if result[1]==user_id:
            ret.append({'message_id': result[0], 'sender': True, 'content': result[2],'time':str(result[3])})
        else:
            ret.append({'message_id': result[0], 'sender': False, 'content': result[2],'time': str(result[3])})
            sql = "update private_message set is_read = 1 where message_id="+str(result[0])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.close()
                traceback.print_exc()
                return False
    return ret

def send_message(sender_name:str,receiver_name:str,content:str):
    if (not sender_name) or (not receiver_name) or (not content):
        return False
    if not content or sender_name==receiver_name:
        return False
    db = mysql.connector.connect(host = "localhost",user = mysql_user,passwd = mysql_password,database = database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '" + sender_name + "'"
    try:cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        return False
    sender_id = result[0][0]
    sql = "select user_id from user_information where user_name = '" + receiver_name + "'"
    try:cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if not result:
        db.close()
        return False
    receiver_id = result[0][0]
    sql = "select count(*) from friend where user_id="+str(sender_id)+" and friend_id="+str(receiver_id)
    try:cursor.execute(sql)
    except:
        db.close()
        traceback.print_exc()
        return False
    result = cursor.fetchall()
    if result[0][0]==0:
        sql = "insert into friend(user_id,friend_id) values("+str(sender_id)+","+str(receiver_id)+")"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.close()
            traceback.print_exc()
            return False
        sql = "insert into friend(user_id,friend_id) values("+str(receiver_id)+","+str(sender_id)+")"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.close()
            traceback.print_exc()
            return False
    sql = "insert into private_message(sender_id,receiver_id,content,time) values("+str(sender_id)+","+str(receiver_id)+",'"+content+"',now())"
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.close()
        traceback.print_exc()
        return False

def delete_post(post_id:str):
    if not post_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "update post set is_delete = 1 where post_id = %s" % (post_id)
    try:
        cursor.execute(sql)
        sql1 = "select author_id from post where post_id = %s" % (post_id)
        cursor.execute(sql1)
        author_id = (cursor.fetchall())[0][0]
        sql2 = "update user_information set post_count=post_count-1 where user_id = %s" % (str(author_id))
        cursor.execute(sql2)
        db.commit()
        db.close()
        return True
    except:
        db.close()
        traceback.print_exc()
        return False

def delete_comment(comment_id:str):
    if not comment_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "update comment set is_delete = 1 where comment_id = %s" % (comment_id)
    try:
        cursor.execute(sql)
        sql1 = "select post_id from comment where comment_id = %s" % (comment_id)
        cursor.execute(sql1)
        post_id = (cursor.fetchall())[0][0]
        sql2 = "update post set comment_count=comment_count-1 where post_id = %s" % (str(post_id))
        cursor.execute(sql2)
        db.commit()
        db.close()
        return True
    except:
        db.close()
        traceback.print_exc()
        return False

def like_post(user_name:str,post_id:str):
    if not user_name or not post_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql1 = "insert into post_like values(%s,%s,1)" % (post_id,user_id)
    sql = "select * from post_like where post_id=%s and user_id=%s" % (post_id,user_id)
    try:
        cursor.execute(sql)
    except:
        traceback.print_exc()
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        if result[0][2]==0:
            sql2 = "update post set like_count=like_count+1 where post_id = %s" % (post_id)
            sql4 = "update post_like set is_like=1 where user_id=%s and post_id=%s" % (user_id, post_id)
            try:
                cursor.execute(sql2)
                cursor.execute(sql4)
                db.commit()
                db.close()
                return {"like":True}
            except:
                traceback.print_exc()
                db.close()
                return False
        else:
            sql3 = "update post set like_count=like_count-1 where post_id = %s" % (post_id)
            sql5 = "update post_like set is_like=0 where user_id=%s and post_id=%s" % (user_id, post_id)
            try:
                cursor.execute(sql3)
                cursor.execute(sql5)
                db.commit()
                db.close()
                return {"like":False}
            except:
                traceback.print_exc()
                db.close()
                return False
    else:
        try:
            sql2 = "update post set like_count=like_count+1 where post_id = %s" % (post_id)
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return {"like":True}
        except:
            traceback.print_exc()
            db.close()
            return False

def dislike_post(user_name:str,post_id:str):
    if not user_name or not post_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql1 = "insert into post_dislike values(%s,%s,1)" % (post_id,user_id)
    sql = "select * from post_dislike where post_id=%s and user_id=%s" % (post_id,user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        if result[0][2]==0:
            sql2 = "update post set dislike_count=dislike_count+1 where post_id = %s" % (post_id)
            sql4 = "update post_dislike set dislike=1 where user_id=%s and post_id=%s" % (user_id, post_id)
            #sql6 = "select post_id from post_like where user_id=%s and post_id=%s and like=1" % (user_id,post_id)
            try:
                '''cursor.execute(sql6)
                result = cursor.fetchall()
                if result:
                    sql3 = "update post set like_count=like_count-1 where post_id = %s" % (post_id)
                    sql5 = "update post_like set like=0 where user_id=%s and post_id=%s" % (user_id, post_id)
                    cursor.execute(sql3)
                    cursor.execute(sql5)'''
                cursor.execute(sql2)
                cursor.execute(sql4)
                db.commit()
                db.close()
                return {"dislike":True}
            except:
                traceback.print_exc()
                db.close()
                return False
        else:
            sql3 = "update post set dislike_count=dislike_count-1 where post_id = %s" % (post_id)
            sql5 = "update post_dislike set dislike=0 where user_id=%s and post_id=%s" % (user_id, post_id)
            try:
                cursor.execute(sql3)
                cursor.execute(sql5)
                db.commit()
                db.close()
                return {"dislike":False}
            except:
                traceback.print_exc()
                db.close()
                return False
    else:
        try:
            sql2 = "update post set dislike_count=dislike_count+1 where post_id = %s" % (post_id)
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return {"dislike":True}
        except:
            db.close()
            return False

def like_comment(user_name:str,comment_id:str):
    if not user_name or not comment_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql1 = "insert into comment_like values(%s,%s,1)" % (comment_id, user_id)
    sql = "select * from comment_like where comment_id=%s and user_id=%s" % (comment_id, user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        if result[0][2] == 0:
            sql2 = "update comment set like_count=like_count+1 where comment_id = %s" % (comment_id)
            sql4 = "update comment_like set is_like=1 where user_id=%s and comment_id=%s" % (user_id, comment_id)
            try:
                cursor.execute(sql2)
                cursor.execute(sql4)
                db.commit()
                db.close()
                return {"like": True}
            except:
                db.close()
                return False
        else:
            sql3 = "update comment set like_count=like_count-1 where comment_id = %s" % (comment_id)
            sql5 = "update comment_like set is_like=0 where user_id=%s and comment_id=%s" % (user_id, comment_id)
            try:
                cursor.execute(sql3)
                cursor.execute(sql5)
                db.commit()
                db.close()
                return {"like": False}
            except:
                db.close()
                return False
    else:
        try:
            sql2 = "update comment set like_count=like_count+1 where comment_id = %s" % (comment_id)
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return {"like": True}
        except:
            db.close()
            return False

def dislike_comment(user_name:str,comment_id:str):
    if not user_name or not comment_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql1 = "insert into comment_dislike values(%s,%s,1)" % (comment_id, user_id)
    sql = "select * from comment_dislike where comment_id=%s and user_id=%s" % (comment_id, user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        if result[0][2] == 0:
            sql2 = "update comment set dislike_count=dislike_count+1 where comment_id = %s" % (comment_id)
            sql4 = "update comment_dislike set dislike=1 where user_id=%s and comment_id=%s" % (user_id, comment_id)
            #sql6 = "select comment_id from comment_like where user_id=%s and comment_id=%s and like=1" % (user_id, comment_id)
            try:
                '''cursor.execute(sql6)
                result = cursor.fetchall()
                if result:
                    sql3 = "update comment set like_count=like_count-1 where comment_id = %s" % (comment_id)
                    sql5 = "update comment_like set like=0 where user_id=%s and comment_id=%s" % (user_id, comment_id)
                    cursor.execute(sql3)
                    cursor.execute(sql5)'''
                cursor.execute(sql2)
                cursor.execute(sql4)
                db.commit()
                db.close()
                return {"dislike": True}
            except:
                db.close()
                return False
        else:
            sql3 = "update comment set dislike_count=dislike_count-1 where comment_id = %s" % (comment_id)
            sql5 = "update comment_dislike set dislike=0 where user_id=%s and comment_id=%s" % (user_id, comment_id)
            try:
                cursor.execute(sql3)
                cursor.execute(sql5)
                db.commit()
                db.close()
                return {"dislike": False}
            except:
                db.close()
                return False
    else:
        try:
            sql2 = "update comment set dislike_count=dislike_count+1 where comment_id = %s" % (comment_id)
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return {"dislike": True}
        except:
            db.close()
            return False

def post_collect(user_name:str,post_id:str):
    if not user_name or not post_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql1 = "insert into post_collect(post_id,user_id) values(%s,%s)" % (post_id, user_id)
    sql2 = "update post set collect_count = collect_count+1 where post_id = %s" % (post_id)
    sql = "select * from post_collect where post_id=%s and user_id=%s" % (post_id, user_id)
    try:
        cursor.execute(sql)
    except:
        traceback.print_exc()
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        db.close()
        return False
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.commit()
        db.close()
        return {"collect":True}
    except:
        traceback.print_exc()
        db.close()
        return False

def post_remove_collect(user_name:str,post_id:str):
    if not user_name or not post_id:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    try:
        sql = "select user_id from user_information where user_name='" + user_name + "'"
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str((cursor.fetchall())[0][0])
    sql1 = "delete from post_collect where post_id = %s and user_id = %s" % (post_id,user_id)
    sql2 = "update post set collect_count=collect_count-1 where post_id = %s" % (post_id)
    try:
        cursor.execute(sql1)
        if cursor.rowcount > 0:
            cursor.execute(sql2)
        db.commit()
        db.close()
        return {"collect":False}
    except:
        db.close()
        return False

def get_user_posts(user_name:str):
    if not user_name:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '%s'" % (user_name)
    user_id=""
    try:
        cursor.execute(sql)
        user_id=str((cursor.fetchall())[0][0])
    except:
        traceback.print_exc()
        db.close()
        return False
    sql = "select post_id from post where author_id = %s order by post_id" % (user_id)
    try:cursor.execute(sql)
    except:
        traceback.print_exc()
        db.close()
        return False
    results = cursor.fetchall()
    ret = []
    for i in results:
        post_id = str(i[0])
        sql = "select post_id,title,content,comment_count,like_count,collect_count from post where is_delete = 0 and post_id=%s" % (post_id)
        try:cursor.execute(sql)
        except:
            traceback.print_exc()
            db.close()
            return False
        re = cursor.fetchall()
        if not re:
            continue
        result = (re)[0]
        if len(result[2]) > 100:
            content = (result[2])[0:100]
        else:
            content = result[2]
        if len(result[1]) > 15:
            title = (result[1])[0:15]
        else:
            title = result[1]
        comment_count = str(result[3])
        like_count = str(result[4])
        collect_count = str(result[5])
        ret.append({'post_id': result[0], 'title': title, 'content': content, 'comment_count': comment_count, 'like_count': like_count,'collect_count':collect_count})
    db.close()
    return ret

def get_collect_posts(user_name:str):
    if not user_name:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '%s'" % (user_name)
    user_id=""
    try:
        cursor.execute(sql)
        user_id=str((cursor.fetchall())[0][0])
    except:
        db.close()
        return False
    sql = "select post_id from post_collect where user_id=%s order by collect_time" % (user_id)
    try:cursor.execute(sql)
    except:
        db.close()
        return False
    results = cursor.fetchall()
    ret = []
    for i in results:
        post_id = str(i[0])
        sql = "select post_id,title,content,comment_count,like_count,collect_count from post where is_delete = 0 and post_id=%s" % (post_id)
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        re = cursor.fetchall()
        if not re:
            continue
        result = (re)[0]
        if len(result[2]) > 100:
            content = (result[2])[0:100]
        else:
            content = result[2]
        if len(result[1]) > 15:
            title = (result[1])[0:15]
        else:
            title = result[1]
        comment_count = str(result[3])
        like_count = str(result[4])
        collect_count = str(result[5])
        ret.append({'post_id': result[0], 'title': title, 'content': content, 'comment_count': comment_count,
                    'like_count': like_count,'collect_count':collect_count})
    db.close()
    return ret

def search_post(word:str):
    if not word:
        return False
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select post_id from post where title like '%"+word+"%' order by post_id desc"
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    results = cursor.fetchall()
    ret = []
    for i in results:
        post_id = str(i[0])
        sql = "select post_id,title,content,comment_count,like_count,collect_count from post where is_delete = 0 and post_id=%s" % (post_id)
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        re = cursor.fetchall()
        if not re:
            continue
        result = (re)[0]
        if len(result[2]) > 100:
            content = (result[2])[0:100]
        else:
            content = result[2]
        if len(result[1]) > 15:
            title = (result[1])[0:15]
        else:
            title = result[1]
        comment_count = str(result[3])
        like_count = str(result[4])
        collect_count = str(result[5])
        ret.append({'post_id': result[0], 'title': title, 'content': content, 'comment_count': comment_count,
                    'like_count': like_count,'collect_count':collect_count})
    db.close()
    return ret

def search_sex(user_name:str):
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select sex from user_information where user_name = %s" % (user_name)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        db.close()
        return result[0][0]
    else:
        db.close()
        return False

def hot_new_index_update():
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select post_id,post_time,browse_count,like_count,collect_count,dislike_count from post"
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    results = cursor.fetchall()
    for result in results:
        time_stamp = int((result[1]).timestamp())
        now_time_stamp = int(time.time())
        time_index = 86400-(now_time_stamp-time_stamp)
        if time_index<0:
            time_index = 0
        time_index = ((time_index)//(8640))+1
        reco_index = result[2]+result[3]*2+result[4]*10-result[5]*5
        if reco_index<1:
            reco_index=1
        hot_new_index = str(time_index*reco_index)
        sql = "update post set hot_new_index=%s where post_id=%s" % (hot_new_index,str(result[0]))
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
    try:
        db.commit()
        db.close()
        return True
    except:
        db.close()
        return False

def select_hot_post():
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select post_id,title,comment_count,like_count,board,hot_new_index,collect_count from post order by hot_new_index desc"
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    ret = []
    results = cursor.fetchall()
    for result in results:
        if len(result[1]) > 15:
            title = (result[1])[0:15]
        else:
            title = result[1]
        ret.append({"post_id":str(result[0]),"title":title,"comment_count":str(result[2]),"like_count":str(result[3]),"board":result[4],"browse_count":str(result[5]),"collect_count":str(result[6])})
    return ret

def post_report(user_name:str,post_id:str,report_reason:str):
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '%s'" % (user_name)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        user_id = str(result[0][0])
    else:
        db.close()
        return False
    sql = "select post_id from post_report where post_id = %s and user_id = %s" % (post_id,user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        db.close()
        return {"message":"已经举报过了"}
    else:
        sql1 = "insert into post_report(user_id,post_id,report_time,report_reason) values (%s,%s,now(),'%s')" % (user_id,post_id,report_reason)
        sql2 = "update post set report_count = report_count+1 where post_id = %s" % (post_id)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return {"message":"举报成功"}
        except:
            db.close()
            traceback.print_exc()
            return False

def comment_report(user_name:str,comment_id:str,report_reason:str):
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '%s'" % (user_name)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        user_id = str(result[0][0])
    else:
        db.close()
        return False
    sql = "select comment_id from comment_report where comment_id = %s and user_id = %s" % (comment_id,user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        db.close()
        return {"message":"已经举报过了"}
    else:
        sql1 = "insert into comment_report(user_id,comment_id,report_time,report_reason) values (%s,%s,now(),'%s')" % (user_id,comment_id,report_reason)
        sql2 = "update comment set report_count = report_count+1 where comment_id = %s" % (comment_id)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return {"message":"举报成功"}
        except:
            db.close()
            return False

def select_friend_anonymous(name:str,who:str):
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql1 = "select user_id from user_information where user_name = '%s'" % (name)
    sql2 = "select user_id from user_information where user_name = '%s'" % (who)
    try:
        cursor.execute(sql1)
        user_1 = str(cursor.fetchall()[0][0])
        cursor.execute(sql2)
        user_2 = str(cursor.fetchall()[0][0])
    except:
        db.close()
        return False
    sql = "select is_anonymous from friend where user_id = %s and friend_id = %s" % (user_1,user_2)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    db.close()
    if result:
        if result[0][0]==0:
            return True
    return False

def set_chat_anonymous(name:str,who:str):
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql1 = "select user_id from user_information where user_name = '%s'" % (name)
    sql2 = "select user_id from user_information where user_name = '%s'" % (who)
    try:
        cursor.execute(sql1)
        user_1 = str(cursor.fetchall()[0][0])
        cursor.execute(sql2)
        user_2 = str(cursor.fetchall()[0][0])
    except:
        db.close()
        return False
    sql = "select is_anonymous from friend where user_id = %s and friend_id = %s" % (user_1, user_2)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    result = cursor.fetchall()
    if result:
        sql1 = "update friend set is_anonymous = 0 where user_id = %s and friend_id = %s" % (user_1,user_2)
        sql2 = "update friend set is_anonymous = 0 where user_id = %s and friend_id = %s" % (user_2,user_1)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False
    else:
        sql1 = "insert into friend(user_id,friend_id,is_anonymous) values(%s,%s,0)" % (user_1,user_2)
        sql2 = "insert into friend(user_id,friend_id,is_anonymous) values(%s,%s,0)" % (user_2,user_1)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

def select_report():
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql1 = "select user_id,post_id,report_time,report_reason from post_report where is_handle = 0"
    sql2 = "select user_id,comment_id,report_time,report_reason from comment_report where is_handle = 0"
    ret = []
    try:
        cursor.execute(sql1)
    except:
        db.close()
        return False
    results = cursor.fetchall()
    for result in results:
        post_id = str(result[1])
        sql = "select title,content from post where post_id = %s" % (post_id)
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        re = cursor.fetchall()
        title = re[0][0]
        content = re[0][1]
        if len(title)>15:
            title = title[0:15]
        if len(content)>100:
            content = content[0:100]
        user_id = str(result[0])
        sql = "select user_name from user_information where user_id = %s" % (user_id)
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        reporter_name = str(cursor.fetchall()[0][0])
        ret.append({"type":"post","reporter_name":reporter_name,"reporter_id":str(result[0]),"post_id":str(result[1]),"report_time":(result[2]).strftime('%Y-%m-%d %H:%M'),"report_reason":result[3],"title":title,"content":content})
    try:
        cursor.execute(sql2)
    except:
        db.close()
        return False
    results = cursor.fetchall()
    for result in results:
        comment_id = str(result[1])
        sql = "select content,comment_time from comment where comment_id = %s" % (comment_id)
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        re = cursor.fetchall()
        content = re[0][0]
        comment_time = re[0][1].strftime('%Y-%m-%d %H:%M')
        if len(content)>100:
            content = content[0:100]
        user_id = str(result[0])
        sql = "select user_name from user_information where user_id = %s" % (user_id)
        try:
            cursor.execute(sql)
        except:
            db.close()
            return False
        reporter_name = str(cursor.fetchall()[0][0])
        ret.append({"type": "comment", "reporter_name":reporter_name,"reporter_id": str(result[0]), "comment_id": str(result[1]),
                    "report_time": (result[2]).strftime('%Y-%m-%d %H:%M'), "report_reason": result[3],"content":content,"comment_time":comment_time})
    db.close()
    return ret

def handle_report(way:int,type:str,id:str,reporter_id:str):
    if way==0:
        if type=="post":
            if not delete_post(id):
                return {"message":"处理失败"}
        else:
            if not delete_comment(id):
                return {"message":"处理失败"}
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    if type=="post":
        sql = "update post_report set is_handle = 1 where post_id=%s and user_id=%s" % (id,reporter_id)
    else:
        sql = "update comment_report set is_handle = 1 where comment_id=%s and user_id=%s" % (id, reporter_id)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return {"message":"处理成功"}
    except:
        db.close()
        return {"message":"处理失败"}

def is_administrator(user_name:str):
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information where user_name = '%s'" % (user_name)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    user_id = str(cursor.fetchall()[0][0])
    sql = "select is_administrator from user_information where user_id = %s" % (user_id)
    try:
        cursor.execute(sql)
    except:
        db.close()
        return False
    is_administrator = cursor.fetchall()[0][0]
    if is_administrator==0:
        return False
    else:
        return True

'''def alter_all_password():
    db = mysql.connector.connect(host="localhost", user=mysql_user, passwd=mysql_password, database=database_name)
    cursor = db.cursor()
    sql = "select user_id from user_information"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        user_id = str(result[0])
        sql = "select user_password from user_information where user_id = %s" % (user_id)
        cursor.execute(sql)
        password = (cursor.fetchall())[0][0]
        h1 = hashlib.md5()
        h1.update(password.encode(encoding = 'utf-8'))
        password = h1.hexdigest()
        sql = "update user_information set user_password = '%s' where user_id = %s" % (password,user_id)
        cursor.execute(sql)
        db.commit()'''

