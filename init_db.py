import sqlite3
import json

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

with open('hackers.json') as d:
    data = json.load(d)

# print(data)
id = 1

for hacker in data:
    connection.execute("""
            INSERT INTO hackers (id, name, company, email, phone) VALUES (?,?,?,?,?)
        """, (id, hacker['name'], hacker['company'], hacker['email'], hacker['phone']))
    for skill in hacker['skills']:
        connection.execute("""
            INSERT INTO skills (skill, rating, hacker) VALUES (?,?,?)
            ON CONFLICT (skill, hacker) DO UPDATE SET rating=?
        """, (skill['skill'], skill['rating'], id, skill['rating']))
    id+=1

connection.commit()
connection.close()