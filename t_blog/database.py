from sqlalchemy import create_engine, insert
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqldb://t_blog:dbpass@localhost/t_blog?charset=utf8mb4', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from t_blog.models import *

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
    new_admin = User(username='admin', password='admin', nickname='admin', email='admin@t_blog.com')
    default_category = Category(name='Uncategorized')
    # db_session.add(new_admin)
    db_session.add(default_category)
    db_session.commit()

def insert_article(title=None, content=None, author=None, category=None):
    new_article = Article(title=title.encode('utf-8'), content=content.encode('utf-8'), author=author, category=category)
    db_session.add(new_article)
    db_session.commit()

def get_article(id):
    return db_session.query(Article).filter(Article.id == id).first()

def get_articles():
    return db_session.query(Article).order_by(Article.id.desc()).limit(10).all()

def get_author_name(id):
    return db_session.query(User).filter(User.id == id).first().nickname

def get_category_name(id):
    return db_session.query(Category).filter(Category.id == id).first().name