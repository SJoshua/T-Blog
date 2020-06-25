import datetime
from sqlalchemy import Column, Integer, String, DateTime, Table, Boolean, Text, ForeignKey
from .database import Base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import login_manager

class Article(Base):
    __tablename__ = 'tb_articles'
    id = Column(Integer, primary_key=True)
    title = Column(Text(collation='utf8mb4_unicode_ci'))
    date = Column(DateTime)
    content = Column(Text(collation='utf8mb4_unicode_ci'))
    author = Column(Integer, ForeignKey('tb_users.id'))
    category = Column(Integer, ForeignKey('tb_categories.id'))
    
    def __init__(self, title=None, content=None, author=None, category=None):
        self.title = title
        self.content = content
        self.author = author
        self.category = category
        self.date = datetime.datetime.now()

    def __repr__(self):
        return '<Article %r>' % (self.id)

class User(Base, UserMixin):
    __tablename__ = 'tb_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(60, collation='utf8mb4_unicode_ci'), unique=True)
    password = Column(String(255))
    nickname = Column(String(60, collation='utf8mb4_unicode_ci'))
    email = Column(String(100), unique=True)

    def __init__(self, username=None, password=None, nickname=None, email=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

class Category(Base):
    __tablename__ = 'tb_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50, collation='utf8mb4_unicode_ci'), unique=True)
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)

class Tag(Base):
    __tablename__ = 'tb_tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50, collation='utf8mb4_unicode_ci'), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % (self.name)

class Tag_Relation(Base):
    __tablename__ = 'tb_tag_relations'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('tb_articles.id'))
    tag_id = Column(Integer, ForeignKey('tb_tags.id'))
    
    def __init__(self, article_id=None, tag_id=None):
        self.article_id = article_id
        self.tag_id = tag_id
    
    def __repr__(self):
        return '<Tag_Relation %r:%r>' % (article_id, tag_id)        

class Comment(Base):
    __tablename__ = 'tb_comments'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('tb_articles.id'))
    author = Column(String(50, collation='utf8mb4_unicode_ci'))
    email = Column(String(50))
    content = Column(Text(collation='utf8mb4_unicode_ci'))
    date = Column(DateTime)
    ip = Column(String(50))
    approved = Column(Boolean)
    
    def __init__(self, article_id=None, author=None, email=None, content=None, ip=None, approved=True):
        self.article_id = article_id
        self.author = author
        self.email = email
        self.content = content
        self.ip = ip
        self.approved = approved
        self.date = datetime.datetime.now()

    def __repr__(self):
        return '<Comment %r>' % (self.id)

class Setting(Base):
    __tablename__='tb_settings'
    id = Column(Integer, primary_key=True)
    key = Column(String(50, collation='utf8mb4_unicode_ci'))
    value = Column(Text(collation='utf8mb4_unicode_ci'))

    def __init__(self,key=None,value=None):
        self.key=key
        self.value=value

    def __repr__(self):
        return '<Setting %r>' % (self.id)

class Articlemeta(Base):
    __tablename__='tb_articlesmeta'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('tb_articles.id'))
    key=Column(String(50, collation='utf8mb4_unicode_ci'))
    value = Column(Text(collation='utf8mb4_unicode_ci'))

    def __init__(self,article_id=None,key=None,value=None):
        self.article_id=article_id
        self.key=key
        self.value=value

    def __repr__(self):
        return '<Articlemeta %r>' % (self.id)

class Usermeta(Base):
    __tablename__='tb_usersmeta'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('tb_articles.id'))
    key=Column(String(50, collation='utf8mb4_unicode_ci'))
    value = Column(Text(collation='utf8mb4_unicode_ci'))

    def __init__(self,user_id=None,key=None,value=None):
        self.user_id=user_id
        self.key=key
        self.value=value

    def __repr__(self):
        return '<Usermeta %r>' % (self.id)

class Commentmeta(Base):
    __tablename__='tb_commentsmeta'
    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('tb_articles.id'))
    key=Column(String(50, collation='utf8mb4_unicode_ci'))
    value = Column(Text(collation='utf8mb4_unicode_ci'))

    def __init__(self,comment_id=None,key=None,value=None):
        self.comment_id=comment_id
        self.key=key
        self.value=value

    def __repr__(self):
        return '<Commentmeta %r>' % (self.id)