from collections import defaultdict
import pymongo
import json

metricDict = ['training_loss', 'training_accuracy', 'test_loss', 'test_accuracy']

def extractMetric(metric):
    # Connexion mongodb
    client = pymongo.MongoClient("localhost", 6534, username="fedn_admin", password="password")

    # Sélection db fedn-test-network
    db = client["fedn-test-network"]

    # Requête sur la collection control.status
    docs = db["control.status"].find({'type': 'MODEL_VALIDATION'})

    model_trail = db["control.model"].find_one({'key': 'model_trail'})
    model_trail_ids = model_trail['model']
    print(model_trail_ids)
    validations = defaultdict(list)

    # Lecture des métriques
    for doc in docs:
        # Récupération du champ data du document
        e = json.loads(doc["data"])
        # Récupération du champ data de ce champ data
        data = json.loads(e['data'])
        # Récupération de la métric
        validations[e['modelId']].append(float(data[metric]))
    # Make sure validations are plotted in chronological order
    validations_sorted = []
    for model_id in model_trail_ids:
        try:
            validations_sorted.append(validations[model_id])
        except Exception:
            pass
    validations_sorted = [i for i in validations_sorted if i !=[]]
    return validations_sorted

scores = dict.fromkeys(metricDict)
for metric in metricDict:
    scores[metric] = extractMetric(metric)