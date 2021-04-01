import sqlite3
import os
from urllib import request


def db_connect():
    db_path = r"C:\Users\motig\ראשי\ג. מחשבים\Laboratory\Projects\books-downloader\books_urls.db"
    conn = sqlite3.connect(db_path)
    return conn

def get_link(filename, dbconnection):
    base_url = "https://link.springer.com/content/pdf/"
    cursor = dbconnection.cursor()
    full_url = base_url + filename
    query = 'SELECT url FROM raw_data WHERE pdf_url =?'
    result = cursor.execute(query, [full_url,])

    if result.rowcount is not None:
        link = result.fetchall()[0][0]
        return link

    return None

def get_name(link):
    print("Connecting to: " + link)
    response = request.urlopen(link)
    if response.status == 200:
        text = response.read().decode("utf-8")
        name = text.split("<title>")[1].split(" |")[0]
        return name

    return None

def change_name(old, new):
    if os.path.exists(old):
        try:
            os.rename(old,new)
            return True
        except FileExistsError:
            new = new.split(".pdf")[0] + " (1)" + ".pdf"
            return change_name(old, new)
        except OSError:
            new_filename = new.split("books-downloader\\")[1]
            new_filename = [c for c in new_filename if c != ":"]
            new_filename = ''.join(new_filename)
            new = new.split("books-downloader\\")
            new = new[0] + "books-downloader\\" + new_filename
            return change_name(old, new)
        except:
            return None

    return None
    
        
def main():
    books_path = r"C:\users\motig\ראשי\ג. מחשבים\laboratory\projects\books-downloader\books"
    log = ""
    books_list = os.listdir(books_path)

    books = [x for x in books_list if x.startswith("10")]

    db_connection = db_connect()

    ext = ".pdf"

    for book in books:
        link = get_link(book, db_connection)
        if link is not None:
            book_name = get_name(link)
        else:
            print("Error: can't find book's link.\nBook's name: "+book)
            continue

        if book_name is not None:
            changed = change_name(books_path + "\\" + book, books_path + "\\" + book_name + ext)
            if changed:
                print("Changed " + book + " to " + book_name + ".pdf")
            elif changed is None:
                print("Can't change " + book + " To " + book_name)
                log += book + "\n"
        else:
            print("Cant get file name: " + book)
    with open(r"C:\users\motig\ראשי\ג. מחשבים\laboratory\projects\books-downloader\log.txt","w") as log_file:
        log_file.write(log)
    
    print("The end. check this: "+ r"C:\users\motig\ראשי\ג. מחשבים\laboratory\projects\books-downloader\log.txt")
    
    

if __name__ == "__main__":
    main()