# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 06:57:52 2022

@author: admin
"""

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from database import insert_documents_fr
from OptioncarriereFr import scarp_documents



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jobs = scarp_documents()
    insert_documents_fr(jobs)



