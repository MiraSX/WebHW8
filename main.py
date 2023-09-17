import argparse
import json

from connect import connect
from models import Quotes, Authors

parser = argparse.ArgumentParser(description='Library')
parser.add_argument('--action')


def load_json():
    with open ('json/authors.json') as json_file:
        data = json.load(json_file)
        
        for i in data:
            Authors(fullname=i['fullname'], born_date=i['born_date'], born_location=i['born_location'], description=i['description']).save()
    
    with open ('json/qoutes.json') as json_file:
        data = json.load(json_file)
        
        for i in data:
            Quotes(tags=i['tags'], author=i['author'], quote=i['quote']).save()


if __name__ == "__main__":
    load_json()    