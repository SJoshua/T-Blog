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
    Base.metadata.create_all(bind=engine)
    Comment.query.delete()
    Article.query.delete()
    User.query.delete()
    Category.query.delete()
    new_admin = User(username='admin', password='admin', nickname='admin', email='admin@t_blog.com')
    default_category = Category(name='Uncategorized')
    db_session.add(new_admin)
    db_session.add(default_category)
    db_session.commit()

def insert_article(title=None, content=None, author=None, category=None):
    new_article = Article(title=title.encode('utf-8'), content=content.encode('utf-8'), author=author, category=category)
    db_session.add(new_article)
    db_session.commit()

def update_article(article_id=None, title=None, content=None, category=None):
    db_session.query(Article).filter(Article.id == article_id).update({"title": title, "content": content, "category": category})
    db_session.commit()

def drop_article(article_id=None):
    db_session.query(Article).filter(Article.id == article_id).delete()
    db_session.commit()

def get_comment(article_id):
    return db_session.query(Comment).filter(Comment.article_id==article_id).order_by(Comment.id.desc()).limit(10).all()

def get_article(id):
    return db_session.query(Article).filter(Article.id == id).first()

def get_articles():
    return db_session.query(Article).order_by(Article.id.desc()).all()

def get_author_name(id):
    return db_session.query(User).filter(User.id == id).first().nickname

def get_category_name(id):
    return db_session.query(Category).filter(Category.id == id).first().name

def insert_comment(article_id=0,author=None,email=None ,content=None, ip=None,approved=True):
    new_comment = Comment(article_id=article_id,author=author.encode('utf-8'),email=email.encode('utf-8'),content=content.encode('utf-8'),ip=ip.encode('utf-8'),approved=approved)
    db_session.add(new_comment)
    db_session.commit()

def verify_password(username=None, password=None):
    return db_session.query(User).filter(User.username == username and User.password == password).first()

# callback function for flask-login extension
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))