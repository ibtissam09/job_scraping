import pymongo
from pymongo import MongoClient
def insert_documents(docs):
    client = MongoClient(host="localhost", port=27017)
    db = client.jobsDb
    maroc_jobs = db.JobsMaroc
    result = maroc_jobs.insert_many(docs)
    print(f"Multiple tutorials: {result.inserted_ids}")
    client.close()


def insert_documents_fr(docs):
    client = MongoClient(host="localhost", port=27017)
    db = client.jobsDb
    jobs = db.JobsFrance
    result = jobs.insert_many(docs)
    print(f"Multiple tutorials: {result.inserted_ids}")
    client.close()