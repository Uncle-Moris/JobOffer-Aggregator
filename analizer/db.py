import sqlite3, json


def create_table():
    with sqlite3.connect("offers.db") as con:
        cur = con.cursor()
        init_sql = '''CREATE TABLE IF NOT EXISTS offer(
                    offer_id INTEGER PRIMARY KEY,
                    title TEXT,
                    level TEXT,
                    source TEXT,
                    skills TEXT,
                    description TEXT,
                    company_name TEXT,
                    operating_mode TEXT);
                    '''
        cur.execute(init_sql)
        con.commit()


def add_offer(title, level, source, skills, description, company_name, operating_mode):
    """
    Adds a new offer to the database.
    
    Parameters:
    - title (str): The title of the offer.
    - level (str): The level of the offer.
    - source (str): The source of the offer.
    - skills (list of str): The skills required for the offer.
    - description (str): A description of the offer.
    - company_name (str): The name of the company offering the job.
    - operating_mode (str): The operating mode of the job.
    """
    # Serialize skills list to JSON format
    serialized_skills = json.dumps(skills)
    
    # Use 'with' statement to manage the database connection and cursor
    with sqlite3.connect("offers.db") as con:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO offer (title, level, source, skills, description, company_name, operating_mode)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, level, source, serialized_skills, description, company_name, operating_mode))
        con.commit()

if __name__ == "__main__":
    create_table()