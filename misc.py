import json

def ConvertToDic(task, location, date, time):
	dic = {task: {"Location": location, "Date": date, "Time": time}}
	#dic["task"] = task
	#dic["location"] = location
	#dic["date"] = date
	#dic["time"] = time
	return dic
	
def AddToFile(dic):
	with open("data.json", "r+") as file:
		data = json.load(file)
		data.update(dic)
		file.seek(0)
		json.dump(data, file, indent=2)

def GetData():
	with open("data.json", "r") as file:
		data = json.load(file)
	return data