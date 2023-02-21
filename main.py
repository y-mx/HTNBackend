from flask import Flask
import sqlite3
import json
from flask import jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/users/", methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM hackers')
    users = [dict(i) for i in users]
    for user in users:
        skills = conn.execute("""
        SELECT skills.skill, skills.rating 
        FROM hackers INNER JOIN skills 
        ON hackers.id=skills.hacker WHERE hackers.id=?
        """, (str(user['id']),))
        skills = [dict(i) for i in skills]
        user['skills'] = skills
        user.pop('id')
    conn.close()
    return jsonify([dict(i) for i in users])

@app.route("/users/<id>", methods=['GET', 'PUT'])
def get_user(id):
    if request.method == 'GET':
        conn = get_db_connection()
        users = conn.execute("""
        SELECT name, company, email, phone FROM hackers WHERE id=?
        """, (id,)).fetchall()
        user = [dict(i) for i in users][0]
        skills = conn.execute("""
        SELECT skills.skill, skills.rating 
        FROM hackers INNER JOIN skills 
        ON hackers.id=skills.hacker WHERE hackers.id=?""", (id,)).fetchall()
        skills = [dict(i) for i in skills]
        user['skills'] = skills
        conn.close()
        return jsonify(user)
    elif request.method == 'PUT':
        print('PUT')
        data = request.json
        conn = get_db_connection()
        for i in data:
            if i != 'skills':
                conn.execute('UPDATE hackers SET %s=? WHERE id=?'%i, (data[i], id))
            else:
                for j in data[i]:
                    conn.execute("""INSERT INTO skills (skill, rating, hacker) VALUES (?,?,?)
                    ON CONFLICT (skill, hacker) DO UPDATE SET rating=?
                    """, (j['skill'], j['rating'], id, j['rating']))
                
        users = conn.execute("""SELECT name, company, email, phone 
        FROM hackers WHERE id=?""", (id,)).fetchall()
        user = [dict(i) for i in users][0]
        skills = conn.execute("""SELECT skills.skill, skills.rating 
        FROM hackers INNER JOIN skills 
        ON hackers.id=skills.hacker 
        WHERE hackers.id=?""", (id,)).fetchall()
        skills = [dict(i) for i in skills]
        user['skills'] = skills
        conn.commit()
        conn.close()
        return jsonify(user)

    

@app.route("/skills/", methods=['GET'])
def get_skills():
    min_freq  = request.args.get('min_frequency', None)
    max_freq  = request.args.get('max_frequency', None)
    # SELECT skill, COUNT(skill) FROM skills GROUP BY skill HAVING COUNT(skill)>15 AND COUNT(skill)<40 ORDER BY COUNT(skill);
    conn = get_db_connection()
    if min_freq == None and max_freq == None:
        skills = conn.execute("""
        SELECT skill, COUNT(skill) AS frequency FROM skills 
        GROUP BY skill ORDER BY COUNT(skill)
        """).fetchall()
    elif min_freq != None and max_freq == None:
        skills = conn.execute("""
        SELECT skill, COUNT(skill) AS frequency 
        FROM skills GROUP BY skill 
        HAVING COUNT(skill)>=? ORDER BY COUNT(skill)
        """, (int(min_freq),)).fetchall()
    elif max_freq != None and min_freq == None:
        skills = conn.execute("""
        SELECT skill, COUNT(skill) AS frequency 
        FROM skills GROUP BY skill 
        HAVING COUNT(skill)<=? ORDER BY COUNT(skill)
        """,(int(max_freq),)).fetchall()
    else:
        skills = conn.execute("""
        SELECT skill, COUNT(skill) AS frequency 
        FROM skills GROUP BY skill 
        HAVING COUNT(skill)<=? AND COUNT(skill)>=? ORDER BY COUNT(skill)
        """, (int(max_freq),int(min_freq))).fetchall()
    
    conn.commit()
    conn.close()
    skills = [dict(i) for i in skills]
    return jsonify(skills)
