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
    default_category = Category(id=1, name='Uncategorized')
    db_session.add(new_admin)
    db_session.add(default_category)
    db_session.commit()



def insert_article(title=None, content=None, author=None, category=None):
    new_article = Article(title=title.encode('utf-8'), content=content.encode('utf-8'), author=author, category=category)
    db_session.add(new_article)
    db_session.commit()
    return new_article.id

def update_article(article_id=None, title=None, content=None, category=None):
    db_session.query(Article).filter(Article.id == article_id).update({"title": title, "content": content, "category": category})
    db_session.commit()

def drop_article(article_id=None):
    db_session.query(Article).filter(Article.id == article_id).delete()
    db_session.commit()

def insert_comment(article_id=None,author=None,email=None ,content=None, ip=None,approved=True):
    new_comment = Comment(article_id=article_id,author=author.encode('utf-8'),email=email.encode('utf-8'),content=content.encode('utf-8'),ip=ip.encode('utf-8'),approved=approved)
    db_session.add(new_comment)
    db_session.commit()

def update_comment(comment_id=None,author=None,content=None):
    db_session.query(Comment).filter(Comment.id==comment_id).update({"author":author,"content":content})
    db_session.commit()

def drop_comment(comment_id=None):
    db_session.query(Comment).filter(Comment.id==comment_id).delete()
    db_session.commit()

def drop_comments(article_id):
    db_session.query(Comment).filter(Comment.article_id==article_id).delete()

def insert_tag(name=None):
    new_tag = Tag(name=name)
    db_session.add(new_tag)
    db_session.commit()

def update_tag(tag_id=None,name=None):
    db_session.query(Tag).filter(Tag.id==tag_id).update({"name":name})
    db_session.commit()

def drop_tag(tag_id=None):
    db_session.query(Tag).filter(Tag.id==tag_id).delete()
    db_session.commit()

def insert_category(name=None):
    new_category = Category(name=name)
    db_session.add(new_category)
    db_session.commit()

def update_category(category_id=None,name=None):
    db_session.query(Category).filter(Category.id==category_id).update({"name":name})
    db_session.commit()

def drop_category(category_id=None):
    db_session.query(Category).filter(Category.id==category_id).delete()
    db_session.commit()

def insert_tag_relation(article_id=None,tag_id=None):
    new_tag_relation=Tag_Relation(article_id=article_id,tag_id=tag_id)
    db_session.add(new_tag_relation)
    db_session.commit()

def drop_tag_relation(article_id=None):
    db_session.query(Tag_Relation).filter(Tag_Relation.article_id==article_id).delete()
    db_session.commit()

def get_user(user_id):
    return db_session.query(User).filter(User.id==user_id).first()

def get_comment(comment_id):
    return db_session.query(Comment).filter(Comment.id==comment_id).first()

def get_comments(article_id):
    return db_session.query(Comment).filter(Comment.article_id==article_id).order_by(Comment.id.desc()).limit(10).all()

def get_article(id):
    return db_session.query(Article).filter(Article.id == id).first()

def get_articles():
    return db_session.query(Article).order_by(Article.id.desc()).all()

def get_author_name(id):
    return db_session.query(User).filter(User.id == id).first().nickname

def get_category_name(id):
    return db_session.query(Category).filter(Category.id == id).first().name

def get_tag(id):
    return db_session.query(Tag).filter(Tag.id==id).first()

def get_tag_name(id):
    return db_session.query(Tag).filter(Tag.id==id).first()

def get_tags():
    return db_session.query(Tag).order_by(Tag.id.desc()).all()

def get_article_tags(article_id):
    return db_session.query(Tag_Relation).filter(Tag_Relation.article_id==article_id).all()

def get_category(id):
    return db_session.query(Category).filter(Category.id==id).first()

def get_categories():
    return db_session.query(Category).order_by(Category.id.desc()).all()
def get_setting_value(key):
    return db_session.query(Setting).filter(Setting.key == key).first().value

def update_setting(key, value):
    if get_setting_value(key):
        db_session.query(Setting).filter(Setting.key == key).update({"value": value})
    else:
        db_session.add(Setting(key=key, value=value))
    db_session.commit()

def verify_password(username=None, password=None):
    user = db_session.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        return user

# callback function for flask-login extension
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))