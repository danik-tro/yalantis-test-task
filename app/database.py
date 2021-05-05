import databases

DATABASE_URL = 'sqlite:///./prod.db'
database = databases.Database(DATABASE_URL)

