import os


def init_migrations(alembic_directory: str, migrations_directory: str, db_name: str):
    os.system(f'mkdir {alembic_directory}&&cd {alembic_directory}&&alembic init {migrations_directory}')
    replace_files(alembic_directory, migrations_directory, db_name)
    os.system(f'cd {alembic_directory}&&alembic revision --autogenerate -m "Added required table"&&alembic upgrade head')


def replace_files(alembic_directory: str, migrations_directory: str, db_name: str):
    file = open(f'{alembic_directory}/alembic.ini', 'r')
    content = file.read().replace('sqlalchemy.url = driver://user:pass@localhost/dbname',
                                  f'sqlalchemy.url = sqlite:///../{db_name}.db')
    file.close()

    file = open(f'{alembic_directory}/alembic.ini', 'w')
    file.write(content)
    file.close()

    replacement = "from alembic import context\n" \
                  "import sys\n" \
                  "sys.path = ['', '..'] + sys.path[1:]\n" \
                  "from app.courses import courses_metadata\n"

    file = open(f'{alembic_directory}/{migrations_directory}/env.py', 'r')
    content = file.read().replace('from alembic import context\n',
                                  replacement).replace('target_metadata = None\n',
                                                       'target_metadata = [courses_metadata]\n')
    file.close()

    file = open(f'{alembic_directory}/{migrations_directory}/env.py', 'w')
    file.write(content)
    file.close()


if __name__ == "__main__":
    init_migrations('db', "migrations", 'prod')
