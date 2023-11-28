from fastapi import FastAPI

from datetime import datetime

from pymongo import MongoClient
from passwords import STR_CONN

cursor = MongoClient(STR_CONN)
db = cursor.final_project

app = FastAPI()

@app.get("/")
def index():
    return {"Usage": "todo"}

# --- GET DICTIOS ---

@app.get("/video")
def video():
	elements = list(db.video.find())
	return elements

@app.get("/creator")
def creator():
	elements = list(db.creator.find())
	return elements

@app.get("/users")
def users():
	elements = list(db.user.find({}, {'_id': 1, 'last_update': 1}))
	return elements

@app.get("/messages")
def messages():
	elements = list(db.message.find())
	return elements

@app.get("/messages/{sent}")
def messages(sent):
	if sent == 'positive':
		sent = 'POS'
	elif sent == 'neutral':
		sent = 'NEU'
	elif sent == 'negative':
		sent = 'NEG'
	else:
		raise HTTPException(status_code=400, detail='Only "positive", "negative" or "neutral" for sentiment analysis.')

	elements = list(db.message.find({'sentiment_analysis': sent}, {}))
	return elements

@app.get("/messages_by_day/{dia}")
def messages_by_day(dia: int):
	start_date = datetime.now().replace(day=dia, hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date.replace(day=(dia + 1))

	elements = list(db.message.find({"date": {"$gte": start_date, "$lt": end_date}}, {}))

	return elements

# -------- REVISAR PORQUE NO FURULA POR ALGÚN MOTIVO LLORARÉ

@app.get("/messages_by_day_and_sent/{param}")
def messages_by_day_and_sent(param):
	param = param.split('-')
	
	dia = int(param[0])
	sent = param[1]

	start_date = datetime.now().replace(day=dia, hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date.replace(day=(dia + 1))

	if sent == 'positive':
		sent = 'POS'
	elif sent == 'neutral':
		sent = 'NEU'
	elif sent == 'negative':
		sent = 'NEG'
	else:
		raise HTTPException(status_code=400, detail='Only "positive", "negative" or "neutral" for sentiment analysis.')

	elements = list(db.message.find({"date": {"$gte": start_date, "$lt": end_date}, 'sentiment_analysis': sent}, {}))
	return elements

# --- GET COUNTS ---

@app.get("/video_count")
def count_total_vids():
	elements = list(db.video.find())
	return {"Video Count": len(elements)}

@app.get("/user_count")
def count_total_users():
	elements = list(db.user.find())
	return {"User count": len(elements)}

@app.get("/message_count")
def count_total_messages():
	elements = list(db.message.find())
	return {"Video count": len(elements)}

# --- try this later ---

# param == f"{sent}-{day}-{stime}-{etime} -- for everything: "POSNEGNEU-0-0-1000"

def user(param):
	params = param.split(-)

	users = list(db.user.find())

	if param[1] == '0':
		messages = list(db.message.find({'sentiment_analysis': {'$in': params[0]},
						 'timestamp': { '$gt':  params[2], '$lt': params[3]}})
			       )
	else:
		date = datetime.now().replace(day=int(param[1], hour=0, minute=0, second=0, microsecond=0)
		messages = list(db.message.find({'sentiment_analysis': {'$in': params[0]},
						'timestamp': { '$gt':  params[2], '$lt': params[3]},
						'date': date})
	       )

	# count = 0
	# for user in users:
	# 	for message in messages:
	# 		if user.id == message.user_id:
	# 			count += 1
	# 			break
	# return {"User count": count}

	# documents_to_update = collection.find({"timestam": {"$exists": True}})
	# updates = []
	
	# for doc in documents_to_update:
	#     new_doc = doc.copy()
	#     new_doc["timestamp"] = doc["timestam"]
	#     del new_doc["timestam"]
	#     updates.append(UpdateOne({"_id": doc["_id"]}, {"$set": new_doc}))
	
	# # Ejecutar las actualizaciones en lotes
	# if updates:
	#     result = collection.bulk_write(updates)
	#     print(f"Se han actualizado {result.modified_count} documentos")
	# else:
	#     print("No se encontraron documentos para actualizar")


def message(param):
	params = param.split(-)

	if param[1] == '0':
		messages = list(db.message.find({'sentiment_analysis': {'$in': params[0]},
						 'timestamp': { '$gt':  params[2], '$lt': params[3]}})
			       )
	else:
		date = datetime.now().replace(day=int(param[1], hour=0, minute=0, second=0, microsecond=0)
		messages = list(db.message.find({'sentiment_analysis': {'$in': params[0]},
						'timestamp': { '$gt':  params[2], '$lt': params[3]},
						'date': date})
	       )

		
	result ={
		'count': len(messages),
		'messages': messages
		}
	return result