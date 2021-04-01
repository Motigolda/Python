import os, sqlite3
from urllib import request
class screen:
    @staticmethod
    def clear():
        x = os.system('cls')
        del(x)

class downloader:
    @staticmethod
    def download(url, bytes_per_time = 16192 * 2):
        # make the request:
        web_response = request.urlopen(url)
        if(web_response.length == 0 or web_response.status != 200):
            return -1

        filelength =  web_response.length
        packets = filelength // bytes_per_time
        if (filelength % bytes_per_time > 0):
            packets += 1
        
        binary = list()
        current = web_response.read(bytes_per_time)
        while(current != b''):
            screen.clear()
            print("Downloading: "+url+"\nDownloaded part: " + str(int(len(binary) / packets * 100)) + "%")
            binary.append(current)
            current = web_response.read(bytes_per_time)
                
        screen.clear()
        print("Download completed.")
        return binary

class saver:
    # get list of binary and save it into file
    @staticmethod
    def save(binary, path):
        print('Creating file at '+ path + "\n")
        file_handler = open(path, 'wb')
        print('Start saving...\n')
        progress = 0
        for i in binary:
            
            print("\r" + str(int(progress / len(binary) * 100)) + "%", end='')
            file_handler.write(i)
            progress += 1

        screen.clear()
        print('Saved at '+path+ ' successfully.')
        file_handler.close()
        

    
class db:
    def connect(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, query, params=  None):
        if(params == None):
            retval = self.conn.execute(query).fetchall()
        else:
            retval = self.conn.execute(query,params).fetchall()
        return [list(i) for i in retval]

    def update(self, query, params = None):
        if(params == None):
            self.conn.execute(query)
        else:
            self.conn.execute(query,params)
        self.conn.commit()

    def insert(self, query, params = None):
        if(params == None):
            self.conn.execute(query)
        else:
            self.conn.execute(query,params)
        self.conn.commit()

    def delete(self, query, params = None):
        if(params == None):
            self.conn.execute(query)
        else:
            self.conn.execute(query,params)
        self.conn.commit()

def main():
    books_path = r'C:\Users\motig\ראשי\ג. מחשבים\Laboratory\Projects\books-downloader\books\\'
    db_path = r"C:\Users\motig\ראשי\ג. מחשבים\Laboratory\Projects\books-downloader\books_urls.db"
    database = db()
    database.connect(db_path)
    links = database.select("SELECT pdf_url FROM raw_data WHERE downloaded IS NULL")
    links = [''.join(x) for x in links]
    links = list(map(lambda s: s.strip(), links))
    for link in links:
        data = downloader.download(link)
        file_name = link.split('https://link.springer.com/content/pdf/')[1]
        saver.save(data, books_path + file_name)
        database.update("UPDATE raw_data SET downloaded = ? WHERE pdf_url = ?",('true',link))
    
    os.startfile(os.path.realpath(books_path))
    
if __name__ == "__main__":
    main()
