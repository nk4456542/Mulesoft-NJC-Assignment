import sqlite3
from sqlite3 import Error

# Movies a list of tuples to populate the database.
movies = [
    ('Avengers - End Game', 'Robert Downey Jr.',
        'Scarlett Johansenn', '2019', 'Russo Brothers'),
    ('Avengers - Infinity War', 'Robert Downey Jr.',
     'Scarlett Johansenn', '2018', 'Russo Brothers'),
    ('John Wick', 'Keanu Reeves', 'Bridget Maynohan',
     '2014', 'Chad Stahelski'),
    ('John Wick 2', 'Keanu Reeves', 'Bridget Maynohan',
     '2017', 'Chad Stahelski'),
    ('Catch Me If You Can', 'Leonardo DiCaprio',
     'Amy Adams', '2002', 'Steven Spielberg'),
    ('Mimi', 'Pankaj Tripathi', 'Kriti Sanon', '2021', 'Laxman Utekar'),
    ('Inception', 'Leonardo DiCaprio', 'Elliot Page', '2010', 'Christopher Nolan'),
    ('Interstellar', 'Matthew McConaughey',
     'Anne Hathaway', '2014', 'Christopher Nolan'),
    ('The Dark Knight', 'Christian Bale',
     'Anne Hathaway', '2008', 'Christopher Nolan'),
    ('Kong - Skull Island', 'Tom Hiddleston',
     'Brie Larson', '2017', 'Jordan Vogt-Roberts'),
]


def create_connection(db_file):
    """
    create a database connection to a Movie database
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_movie(conn, movie):
    """
    Insert a new Movie into the `movies` table
    :param conn:
    :param project:
    :return: project id
    """
    sql_cmd = '''INSERT INTO movies(movie_name,lead_actor,lead_actress,year_of_release,director_name) VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql_cmd, movie)
    conn.commit()
    return cur.lastrowid


def print_results_from_select(rows):
    if(len(rows) > 0):
        for row in rows:
            print()
            print("****************************************************")
            print(row)
            print()
    else:
        print()
        print("****************************************************")
        print("No Data Found Regarding the Query")
        print("****************************************************")
        print()


def populate_data(movies, conn):
    for movie in movies:
        movie_id = insert_movie(conn, movie)
        print(movie_id)


def menu(conn):
    print()
    print("Enter your choice: ")
    print("1. Query all movies")
    print("2. Query movies by movie name")
    print("3. Query movies by lead actor")
    print("4. Query movies by lead actress")
    print("5. Query movies by year of release")
    print("6. Query movies by director name")
    print("7. Exit")
    print()
    choice = int()
    query = None
    try:
        choice = int(input())
    except:
        return 8, query
    if choice != 1 and choice != 7:
        print("Enter your Query:")
        query = input()
    return choice, query


def query_movie_data(conn, query_param_name=None, query=None):
    """
    Query all rows in the movies table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    if query == None:
        cur.execute("SELECT * FROM movies")
    else:
        cur.execute(f"SELECT * FROM movies WHERE {query_param_name}=?",
                    (query,))
    rows = cur.fetchall()
    print_results_from_select(rows)
    return rows


def main():
    database = "movies.db"
    sql_create_movies_table = """ CREATE TABLE IF NOT EXISTS movies (
                                        id integer PRIMARY KEY,
                                        movie_name text NOT NULL,
                                        lead_actor text NOT NULL,
                                        lead_actress text NOT NULL,
                                        year_of_release text NOT NULL,
                                        director_name text NOT NULL
                                    ); """
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create movies table
        create_table(conn, sql_create_movies_table)

        # Populate movies table
        # populate_data(movies, conn)

        # Execute User Queries
        while True:
            query_param_name = None
            query = None
            choice, query = menu(conn)
            if(choice == 7):
                break
            elif(choice == 1):
                query_param_name = None
            elif(choice == 2):
                query_param_name = "movie_name"
            elif(choice == 3):
                query_param_name = "lead_actor"
            elif(choice == 4):
                query_param_name = "lead_actress"
            elif(choice == 5):
                query_param_name = "year_of_release"
            elif(choice == 6):
                query_param_name = "director_name"
            else:
                print("Invalid choice, Please Choose Again")
                continue
            query_movie_data(conn, query_param_name, query)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
