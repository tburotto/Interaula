import sqlite3
con = sqlite3.connect("dbinteraula.db")
cursor = con.cursor()
usr = "tfburotto"
pswd = "1234567890"
cursor.execute("SELECT * FROM Profesores WHERE username ='" + str(usr) + "' AND password ='" + str(pswd) + "';")
users = cursor.fetchall()
print(users)