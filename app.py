from models import(Base, session, Book, engine)
import csv
from datetime import datetime, date
import time
def menu():
    while True:
        print('''
        \nPROGRAMMING BOOKS
        \r1) Add book
        \r2) View all books
        \r3) Search for book
        \r4) Book Analysis
        \r5) Exit
        ''')
        choice = input("What would you like to do? ")

        if choice in ('1','2','3','4','5'):
            return choice
        else:
            input('''
                \rplease choose one of the options above.
                \rA number from 1-5.
                \rPress enter to try again.''')

#import models
# main menu - add, search, analysis, exit, view
# add books to the database
# edit boooks
# delete books
# search books
# data cleaning
# loop runs program

def clean_date(date_str):
    try:
        return_date = datetime.strptime(date_str, '%B %d, %Y').date()
    except ValueError:
        input('''
        \n******** DATE ERROR ********
        \rThe date format should include a valid Month, Day, Year from the past.
        \rEX: January 24, 2017 
        \r Press enter to try again.
        \r**************************''')
        return
    else:
        return return_date

def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
        \n******** PRICE ERROR ********
        \rThe price should be a number without the currency symbol.
        \rEX: 112.99 
        \r Press enter to try again.
        \r**************************''')
        return
    else:
        return int(price_float * 100)

def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
        \n******** ID ERROR ********
        \rThe ID should be a number.
        \r Press enter to try again.
        \r**************************''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input('''
        \n******** ID ERROR ********
        \rOptions: {options}
        \r Press enter to try again.
        \r**************************''')
            return

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)

        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "1":
            #add book
            title = input('Title: ')
            author = input('Author: ')
            
            date_error = True
            while date_error:
                pub_date = input('Published Date (Ex: October 25, 2017): ')
                pub_date = clean_date(pub_date)
                if type(pub_date) == date:
                    date_error = False

            price_error = True
            while price_error:
                price = input('Price (Ex: 25.34): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            
            new_book = Book(title=title, author=author, published_date=pub_date, price=price)
            session.add(new_book)
            session.commit()
            print('The book was added!')
            time.sleep(1.5)

        elif choice == "2":
            #view books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.published_date} | {book.price}')
            input('\n Press enter to return to the main menu')
        
        elif choice == "3":
            # search books
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            
            id_error = True
            while id_error :
                id_choice = input(f'''
                    \nId Options: {id_options}
                    \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False

            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
                \n{the_book.title} by {the_book.author}
                \rPublished: {the_book.published_date}
                \rPrice: ${the_book.price / 100} ''')
            input('\nPress enter to return to the main menu')

        elif choice == "4":
            # analysis
            pass
        else:
            print('GOODBYE')
            app_running = False



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    #print(type(clean_date('October 25, 2017')))
    
    #for book in session.query(Book):
    #    print(book)