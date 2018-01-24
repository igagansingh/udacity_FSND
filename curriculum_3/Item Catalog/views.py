from models import Base, User, Categories, CategoryItem

from flask import Flask, render_template, url_for

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/')
def index():
	categories = session.query(Categories).filter_by().all()
	items = session.query(CategoryItem).filter_by().limit(5)
	return render_template('index.html', categories=categories, items=items)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)