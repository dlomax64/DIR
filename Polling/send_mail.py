from typing import List
import sys
import os

import yagmail

def parse_data(filename:str) -> List:
    ''' Return a list of Tuples: (name, email, language)

        filename: Name of file. 
        return: List of tuples.
    '''

    data = []

    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        
        for line in lines:
            words = line.split(';')
            user = words[0]
            name = user[:user.find(' ')]
            email = user[user.find('<')+1: -1]
            language = words[-1]

            data.append((name, email, language))

    return data

def send_mail(data:List, boildplate) -> None:
    ''' Send mail to the users. 

        data: List of Tuples (name, email, language)
        return: None
    '''
    addresses = [
        "fdac2021@gmail.com",
        "fdac2022@gmail.com",
        "fdac2023@gmail.com",
        "fdac2024@gmail.com",
        "fdac2025@gmail.com" 
    ]
    
    pins = [
        "tulsgdlrvkrdpdsi",
        "rwejckvcdcyjdsfw",
        "cexeegenygpjqbyo",
        "pbuelfmdbaanqvva",
        "xgfbeyabkwkugqmv" 
    ]

    subject = "Quick poll"

    with open(boilerplate, 'r') as f:
        s = f.read()
        i = 0;

        for d in data:
            message = s
            name, email, languages = d[0], d[1], d[2]

            message = message.replace("USERNAME", name)
            message = message.replace("LANGUAGES", languages)

            with yagmail.SMTP(addresses[i%5], pins[i%5]) as yag:
                try: 
                    yag.send(email, subject, message)
                    print("Sent to ", email)
                except:
                    print("Couldn't send to ", email)
            
            i+=1

if __name__ == "__main__":
    datafile = os.path.abspath(os.path.dirname(__file__)) + "/Authors/day_" + sys.argv[1]
    boilerplate = os.path.abspath(os.path.dirname(__file__)) + "/boilerplate.txt"
    data = parse_data(datafile)

    send_mail(data, boilerplate)