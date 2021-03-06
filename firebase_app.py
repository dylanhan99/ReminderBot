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
pyrebase.__spec__
parentName = "Reminders"
firebaseApp = pyrebase.initialize_app(firebaseConfig)
dbRef = firebaseApp.database()

def Add(task, data):
    try:
        dbRef.child(parentName).child(task).set(data)
        return True
    except:
        return False

def GetVal(task, key):
    try:
        return dbRef.child(parentName).child(task).child(key).get().val()
    except:
        return False

def GetReminder(task):
    try:
        return dbRef.child(parentName).child(task).get().val()
    except:
        return False

def GetReminders():
    try:
        return dbRef.child(parentName).get()
    except:
        return False

def DoesReminderExist(task):
    try:
        if dbRef.child(parentName).child(task).get().val() == None:
            return False
        return True
    except:
        return False

def DoesKeyExist(task, key):
    try:
        if dbRef.child(parentName).child(task).child(key).get().val() == None:
            return False
        return True
    except:
        return False

def Edit(task, data):
    try:
        dbRef.child(parentName).child(task).update(data)
        return True
    except:
        return False

def Remove(task):
    try:
        dbRef.child(parentName).child(task).remove()
        return True
    except:
        return False