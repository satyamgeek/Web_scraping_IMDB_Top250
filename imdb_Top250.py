import bs4
import lxml
import requests
import csv
from csv import writer
import pandas as pd
import sqlite3

url = "https://www.imdb.com/chart/top/"
result = requests.get(url)
soup = bs4.BeautifulSoup(result.text,'lxml')
movies = soup.select('td.titleColumn ')

Movie_title = soup.select('td.titleColumn a')
movie_list = []                                           #Extracting movie titles from the Movie_title
for t in Movie_title:
    Movie_name = t.getText()
    movie_list.append(Movie_name)

release_date = soup.select('span .secondaryInfo')
date_dic = []                                             #Extracting Year from the release_date
for date in release_date:
    Release_d = date.getText()[1:5]
    date_dic.append(Release_d)

site_list = []                                            #Extracting movie_link 
for link in soup.select('td.titleColumn a'):
    site="https://www.imdb.com"+str(link.attrs.get('href'))
    site_list.append(site)

Actor_list = []
Dir_list = []
for dirc in soup.select('td.titleColumn a'):              #Extracting movie director & actor names from the Movie_title
    direc = str(dirc.attrs.get('title'))
    director = direc.split('(dir.),')
    Dir_list.append(director[0])
    Actor_list.append(director[1])

while(True):
    ip = int(input("How do you want to save the Data which is collected CSV(1) or SQLite(2) : "))
    
    if ip == 1:
        file_name = str(input("Enter File Name"))+".csv"
        db = open(file_name, "w")                         #Making a csv file to enter the collected Data
        writer = writer(db)

        for i in range(len(movies)):
            writer.writerow([movie_list[i], date_dic[i], Actor_list[i], Dir_list[i], site_list[i]])
    
        db.close()
  
        file = pd.read_csv(file_name)  
        headerList = ['Movie Name', 'Release Date', 'Actors', 'Director', 'Movie Link']
  
        file.to_csv(file_name, header=headerList, index=False)
  
        file2 = pd.read_csv(file_name)
        
        print("Your File is Saved")
        break
    
    elif ip == 2:
        db_name = str(input("Enter the Database_name : "))
        try:
            sqliteConnection = sqlite3.connect(db_name)   
            sqlite_create_table_query = '''CREATE TABLE Movie_database (          
                                Movie_name TEXT PRIMARY KEY,
                                Release_date INTEGER NOT NULL,
                                Actors TEXT NOT NULL ,
                                Director TEXT NOT NULL,
                                Movie_link TEXT NOT NULL);'''

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            print("SQLite table created")
            for i in range(len(movies)):

                count = cursor.execute("""INSERT INTO Movie_database
                              (Movie_name, Release_date, Actors, Director, Movie_link) 
                               VALUES (?,?,?,?,?)""",
                           (movie_list[i], date_dic[i], Actor_list[i], Dir_list[i], site_list[i])
                          )
            sqliteConnection.commit()
            print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
                print("Error while sqlite creation : ", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is closed")
            ch = str(input("Do you want to Enter a query(Y/N) : "))
            if ch == 'y' or ch == 'Y':
                print("Info : db_name : ",db_name)
                print("Table_name : Movie_database")
                print("Attributes(types) : Movie_name(string), Release_date(int), Actors(str), Director(str), Movie_link(str)")
                #db_path = str(input("Enter the path of the SQLite Database :"))
                query = str(input("Enter Query : "))
                dbfile = db_name
                print(dbfile)
                con = sqlite3.connect(dbfile)

                cur = con.cursor()

                table_list = [a for a in cur.execute(query)] 
                print(table_list)

                con.close()
        
                break
     
            else :
                break
                
        break 
    else :
        print('Invalid Input !')
        