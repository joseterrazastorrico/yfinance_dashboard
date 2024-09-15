import os
from dotenv import load_dotenv
load_dotenv()

username = os.environ['USERNAME']
password = os.environ['PASSWORD']
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['DATABASE']
STR_CONN = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'