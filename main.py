# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from database import insert_documents
from OptioncarriereMa import scarp_documents



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jobs = scarp_documents()
    insert_documents(jobs)
