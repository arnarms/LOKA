import bottle
from bottle import run, route, template, static_file, request, hook, redirect
from beaker.middleware import SessionMiddleware
from functools import wraps
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Text
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
import random

Base = declarative_base()
engine = create_engine('mysql+pymysql://1505982309:ZByy2vtJ7T7Rebmr@tsuts.tskoli.is/1505982309_lverk')

app = bottle.app()
plugin = sqlalchemy.Plugin(engine, keyword='db')
app.install(plugin)

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'jhfkjshgjshgfjfdhfgenejnjvnjfnvjnjsvsljflsjfak',
    'session.httponly': True,
    'session.timeout': 3600 * 24,
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = SessionMiddleware(app, session_opts)

class user(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))

class article(Base):
    __tablename__='article'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    body = Column(Text())
    author = Column(String(25))

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/')
def index(db):
        return template('index_open')

@route('/login')
def login():
    return template('login')

@route('/login', method='POST')
def do_login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = db.query(user).filter(user.username==username).first()
    if result == None:
        redirect('/login')
    if result.password == password:
        request.session['username'] = username
        request.session.save()
        redirect('/')
    else:
        redirect('/login')

@route('/logout')
def logout():
    if 'username' in request.session:
        request.session.delete()
        redirect('/login')