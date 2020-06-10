from sqlalchemy import Column, Integer, String, Table, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(20))
    describe = Column(String(200),nullable=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Tag(Base):
    __tablename__ = 'tag'
    name = Column(String(50), primary_key=True)
    describe = Column(String(200),nullnullable=True)
    
    def __repr__(self):
        return '<Tag %r>' % (self.name)

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(50), primary_key=True)
    
    def __repr__(self):
        return '<Category %r>' % (self.name)

class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    date = Column(String(50))
    content = Column(String(collation='utf8'))
    author_id= Column(String(50),ForeignKey('users.name'))
    Category_name=Column(String(50),ForeignKey('category.name'))
    
    def __repr__(self):
        return '<Blog %r>' % (self.id)

class Set_tag(Base):
    __tablename__ = 'set_tag'
    tag_name=Column(String(50),ForeignKey('tag.name'),primary_key=True)
    blog_id =Column(Integer,ForeignKey('blog.id'),primary_key=True)
        
    def __repr__(self):
        return '<Set_tag %r>' % (self.id)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    blog_id =Column(Integer,ForeignKey('blog.id'))
    content=content = Column(String(collation='utf8'))
    date = Column(String(50))
    ip = Column(String(50))
    author_nickname = Column(String(50))
    father_comment =Column(Integer)   
    
    def __repr__(self):
        return '<Comment %r>' % (self.id)



