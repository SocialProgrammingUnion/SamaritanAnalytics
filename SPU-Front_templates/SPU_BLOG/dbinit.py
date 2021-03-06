import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_blog import app
import sqlalchemy

db_uri = 'mysql://%s:%s@mysql:3306/' % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'])
engine = sqlalchemy.create_engine(db_uri)
conn = engine.connect()
conn.execute("commit")
#conn.execute('SET FOREIGN_KEY_CHECKS = 0;')
#conn.execute("DROP DATABASE " + app.config['BLOG_DATABASE_NAME'])
conn.execute("CREATE DATABASE " + app.config['BLOG_DATABASE_NAME'])
conn.close()


'''
Adding
SET FOREIGN_KEY_CHECKS = 0;
before dropping a database fixes the foreign key constraint problem (as introduced in 4.0.18) for me
'''
