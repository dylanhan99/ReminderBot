import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDkQ8UdL5i5b04_H8Eor6PdvkbfOx47LL0",
    "authDomain": "discord-reminderbot.firebaseapp.com",
    "databaseURL": "https://discord-reminderbot-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "discord-reminderbot",
    "storageBucket": "discord-reminderbot.appspot.com",
    "serviceAccount": "serviceAccountKey.json"#,
    #"messagingSenderId": "689305046691",
    #"appId": "1:689305046691:web:7ff57c715688c11123f916",
    #"measurementId": "G-GBC6YBDGW5"
}

parentName = "Reminders"
firebaseApp = pyrebase.initialize_app(firebaseConfig)
dbRef = firebaseApp.database()

def Add(task, data):
    dbRef.child(parentName).child(task).set(data)

def GetReminders():
    return dbRef.child(parentName).get()
    
#storageRef.child("FeelsGoodMan.png").put("FeelsGoodMan.png")

#firebaseApp = pyrebase.initialize_app(firebaseConfig)
#dbRef = firebaseApp.database()
#task = "Do drugs"
#data = {
#    "Location": "safti",
#    "Date": 19802110,
#    "Time": 2110 
#    }
#dbRef.child(parentName).child(task).set(data)
#
#reminders = dbRef.child(parentName).get()
#for r in reminders.each():
#    print(r.key())
#    print(r.val())