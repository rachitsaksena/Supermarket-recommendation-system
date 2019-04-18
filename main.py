import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import recommendation_model

''' Replace "firestore_credentials.json" with your credentials json file'''
cred = credentials.Certificate('firestore_credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

collection = db.collection(u'transactiondata')

currentTime = datetime.datetime.now()


def on_snapshot(doc_snapshot, changes, read_time):
	for change in changes:
		print("CHANGE DETECTED FOR : {}".format(change.document.id))
		tempdat = change.document.to_dict()

		with open('trx_data.csv', 'a+') as file:
			file.write("{},{}\n".format(tempdat['user'], tempdat['items_bought']))

		with open('recommend_1.csv', 'a+') as file:
			file.write(str(tempdat['user']))

		model = recommendation_model.main()

		''' k is the number of recommendations you want'''
		recom = list(model.recommend(users=[1], k=10).to_numpy()[:, 1])
		recom = [str(int(i)) for i in recom]
		db.collection(u'predictions').document(str(tempdat['user'])).set({'products': "|".join(recom)})


doc_watch = db.collection(u'transactiondata').where(u'timestamp', u'>', currentTime).on_snapshot(on_snapshot)
