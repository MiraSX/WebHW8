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
            author = Authors(fullname=i['fullname'], born_date=i['born_date'], born_location=i['born_location'], description=i['description'])
            author.save()

    with open ('json/qoutes.json') as json_file:
        data = json.load(json_file)
        
        for i in data:
            authors = Authors.objects(fullname=i['author']).first()
            c_id_a = authors.id

            quote = Quotes(tags=i['tags'], author=c_id_a, quote=i['quote'])
            quote.save()

def find():
    while True:
        command = input ("Enter action: ")
        if command == 'exit':
            break

        else:
            args = command.split(':')
            comm = args[0]

            if comm == 'name':
                a = Authors.objects(fullname=args[1]).first()
                quotes = Quotes.objects(author=a.id)
                for quote in quotes:
                    print(quote.quote)

            if comm == 'tag':
                quotes = Quotes.objects(tags=args[1])
                for quote in quotes:
                    print(quote.quote)

            if comm == 'tags':
                for tag in args[1].split(','):
                    quotes = Quotes.objects(tags=tag)
                    for quote in quotes:
                        print(quote.quote)
if __name__ == "__main__":
    if parser.parse_args().action == 'load':
            load_json()
    find()    