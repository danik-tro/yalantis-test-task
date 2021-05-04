import sqlalchemy

courses_metadata = sqlalchemy.MetaData()


courses = sqlalchemy.Table(
    'courses',
    courses_metadata,
    sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.VARCHAR(150)),
    sqlalchemy.Column('start_date', sqlalchemy.DATETIME),
    sqlalchemy.Column('end_date', sqlalchemy.DATETIME),
    sqlalchemy.Column('lectures', sqlalchemy.INTEGER)
)