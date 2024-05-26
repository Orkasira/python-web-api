import requests
import json
import sqlite3

res = requests.get("https://jsonplaceholder.typicode.com/posts")

data = res.json()

# Minimum 4 methods
status_code = res.status_code
headers = res.headers
text = res.text

print(status_code)
print(headers)
print(text)


# Write JSON to file
with open("posts.json", "w") as file:
    json.dump(data, file, indent=2)


# Get data from JSON
for i in data:
    print(i["title"] + "\n" + i["body"] + "\n")


# Create SQLite database
conn = sqlite3.connect("posts.sqlite3")
cursor = conn.cursor()

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              userId INTEGER,
              title VARCHAR(255),
              body TEXT
) """
)

insertable_data = []
for i in data:
    insertable_data.append((i["userId"], i["title"], i["body"]))

cursor.executemany(
    "INSERT INTO posts (userId, title, body) VALUES (?, ?, ?)", insertable_data
)
conn.commit()
