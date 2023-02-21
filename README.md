## About

This is a REST API server built with Flask and SQLite to work with hackathon participants' data.

## Getting Started

Initialize database from hackers.json file
```sh
   python init_db.py
```

Install dependencies
```sh
   pip install -r requirements.txt
```

Start the server with the command
```sh
   flask --app main run --port=3000
```
## Endpoints

Get all users information:

`GET localhost:3000/users/`

Get one user's information:

`GET localhost:3000/users/123`

Where the ID of the users range between 1 and 1000, with the order being the order they are presented in the hackers.json file

Update one user's information:

`PUT localhost:3000/users/123`
with json data
```json
  {
    "phone": "+1 (555) 123 4567"
  }
```

Get skills:
`GET localhost:3000/skills/?min_frequency=5&max_frequency=10`

## Note
- The database does not allow the same user to have multiple skills with the same name. This leads to the information being stored in the initial database being slightly different from the data in the hackers.json file. For example, user Susan Roberts only has one Plotly skill with a rating of 4. I chose to do this since it makes no sense for one user to have two different ratings for the same skill, and this makes inserting and updating skills easier

## Next Steps
There are several ways to expand upon and improve this server:
- Add a database for events and endpoints to query events within a given timeframe, show the number of hackers that have attended an event, and scan a hacker in for the event. The users end points can also show the events an user attended
- Add validators to ensure the emails and phone numbers of hackers are valid
- Add endpoints to show users with specific skills and ratings to facilitate searching for teammates