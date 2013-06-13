#coding=utf8

import os
import re
import sys
import urllib
import logging
from urlparse import urljoin
from datetime import datetime

import utils

from flask import (Flask, render_template, request, redirect,
    url_for, abort, Markup, escape)

app = Flask(__name__)
app.config.from_object(os.environ.get('OPENEM_CONFIG', 'config.dev'))
app.logger.addHandler(logging.StreamHandler(sys.stdout))

import model
db = model.db
db.init_app(app)

# FIXME: create a custom 404 NOT FOUND page

@app.route('/')
def main():
    conversations = model.Conversation.query.filter_by(is_example=True).order_by(model.Conversation.update_time.desc()).all()
    return render_template('landing.html', conversations=conversations)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/conversations/<int:id>/')
@app.route('/conversations/<int:id>/<slug>')
def conversation(id, slug=None):
    conv = model.Conversation.query.get_or_404(id)
    if slug != conv.slug:
        return redirect(url_for('conversation', id=id, slug=conv.slug))
    authorId = request.args.get('author')
    author = model.Author.query.get_or_404(authorId) if authorId else None
    new_message_type = model.Message.TYPE.TALKER if conv.owner is author else model.Message.TYPE.LISTENER
    return render_template(
        'conversation.html', 
        conversation=conv, 
        messages=list(conv.messages), 
        author=author,
        new_message_type=new_message_type
    )

@app.route('/conversations/<int:id>/join', methods=['POST'])
def join_conversation(id, slug=None):
    conv = model.Conversation.query.get_or_404(id)
    name = request.form['name'].strip()
    if not name:
        abort(400)
    author = model.Author(name)
    conv.authors.append(author)
    db.session.commit()
    return redirect(url_for('conversation', id=conv.id, slug=conv.slug, author=author.id), code=303)

@app.route('/conversations/<int:id>/updates')
def conversation_updates(id):
    conv = model.Conversation.query.get_or_404(id)
    author = model.Author.query.get_or_404(request.args.get('author'))
    last_message_id = int(request.args.get('last_message_id', -1, type=int))
    messages = conv.get_updated_messages(last_message_id, author)
    last_message_id = messages[-1].id if messages else last_message_id
    result = utils.jsonify(
        conversation=conv,
        messages=messages, 
        last_message_id=last_message_id
    )
    db.session.commit()
    return result

@app.route('/conversations/<int:id>/post', methods=['POST'])
def post_message(id):
    print request.form['author']
    conv = model.Conversation.query.get_or_404(id)
    author = model.Author.query.get_or_404(request.form['author'])
    text = request.form['text']
    if not text.strip():
        abort(400)
    if (conv.owner != author and conv.status == model.Conversation.STATUS.PENDING):
        conv.status = model.Conversation.STATUS.ACTIVE
    conv.messages.append(model.Message(author, escape(request.form['text'])))
    conv.update_time = datetime.utcnow()
    db.session.commit()
    return 'OK', 201

@app.route('/conversations/new', methods=['GET', 'POST'])
def new_conversation():
    if request.method == 'GET':
        return render_template('new_conversation.html')

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['message']
        if not title or not text:
            abort(400)

        conv = model.Conversation(request.form['title'])
        author = model.Author(request.form['author'], is_owner=True)
        conv.authors.append(author)
        conv.messages.append(model.Message(author, escape(request.form['message'])))
        db.session.add(conv)
        db.session.commit()
        return redirect(url_for('conversation', id=conv.id, slug=conv.slug, author=author.id), code=303)

@app.route('/conversations/all')
def all():
    conversations = model.Conversation.query.order_by(model.Conversation.update_time.desc()).all()
    return render_template('all.html', conversations=conversations)

@app.template_filter('urlencode')
def urlencode_filter(s):
    if isinstance(s, unicode):
        s = s.encode('utf8')
    return Markup(urllib.quote_plus(s))

@app.template_filter('multiline')
def multiline_filter(s):
    s = s or ''
    s = re.sub(r'(\r?\n)', '<br>', s)
    return Markup(s)

@app.template_filter('shorten')
def shorten_filter(s, maxlen=40):
    if len(s) < maxlen:
        return s
    else:
        return s[:maxlen-3] + '...'

def include_raw(filename):
    return Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])
app.jinja_env.globals.update(include_raw=include_raw)

def urldecode(s):
    if isinstance(s, unicode):
        s = s.encode('utf8')
    return urllib.unquote(s).decode('utf8')

def make_external(url):
    return urljoin(request.url_root, url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
