#coding=utf8

import os
import re
import sys
import urllib
import logging
import postmark
from urlparse import urljoin
from datetime import datetime

import utils

from flask import (Flask, render_template, request, session, redirect,
    url_for, abort, Markup, escape)

from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)
app.config.from_object(os.environ.get('OPENEM_CONFIG', 'config.dev'))
app.logger.addHandler(logging.StreamHandler(sys.stdout))

import model
db = model.db
db.init_app(app)

# FIXME: create a custom 404 NOT FOUND page

@app.route('/')
def main():
    user = get_current_user(required=False)
    if user:
        my_updated = len(user.get_my_unread_conversations())
        all_updated = len(user.get_unread_conversations())
        pending = model.Conversation.query.filter_by(status=model.Conversation.STATUS.PENDING).count()
        return render_template('profile.html', my_updated=my_updated, all_updated=all_updated, pending=pending)
    else:
        conversations = model.Conversation.all()
        return render_template('landing.html', conversations=conversations)

@app.route('/updates')
def updated_conversations():
    user = get_current_user()
    return render_template('updates.html', title=u"השיחות שלי", conversations=user.conversations)

@app.route('/all')
def all_conversations():
    conversations = model.Conversation.all()
    return render_template('updates.html', title=u"כל השיחות", conversations=conversations)

@app.route('/pending')
def pending_conversations():
    user = get_current_user()
    conversations = model.Conversation.query.filter_by(status=model.Conversation.STATUS.PENDING)
    return render_template('updates.html', title=u"שיתופים ממתינים", conversations=conversations)

@app.route('/atom')
def main_feed():
    feed = AtomFeed(u'Open Emotion Conversations', feed_url=request.url, url=request.url_root)
    for conv in model.Conversation.query:
        feed.add(conv.title,
                 conv.get_first_message().text,
                 content_type='html',
                 author=conv.owner.name,
                 url=make_external('/conversations/%d' % conv.id),
                 updated=conv.update_time,
                 published=conv.start_time)
    return feed.get_response()

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/anon')
def anon():
    return render_template('anon.html')

@app.route('/listen')
def listen():
    return render_template('listen.html')

@app.route('/hallway')
def hallway():
    return render_template('hallway.html')

@app.route('/pub')
def pub():
    return render_template('pub.html')

@app.route('/conversations/<int:id>/')
@app.route('/conversations/<int:id>/<slug>')
def conversation(id, slug=None):
    user = get_current_user()
    conv = model.Conversation.query.get_or_404(id)
    if slug != conv.slug:
        return redirect(url_for('conversation', _external=True, id=id, slug=conv.slug))
    conv.mark_read(user)
    db.session.commit()
    user_message_type = detect_user_message_type(conv)
    return render_template(
        'conversation.html', 
        conversation=conv, 
        messages=list(conv.messages), 
        user_message_type=user_message_type
    )

@app.route('/conversations/<int:id>/atom')
def conversation_feed(id):
    user = get_current_user()
    conv = model.Conversation.query.get_or_404(id)
    feed = AtomFeed(conv.title, feed_url=request.url, url=request.url_root)
    for message in conv.messages:
        feed.add (
            message.text.splitlines()[0],
            message.text,
            content_type='html',
            author=message.author.name,
            url=request.url_root,
            updated=message.post_time,
            published=message.post_time
        )
    return feed.get_response()

@app.route('/conversations/<int:id>/updates')
def conversation_updates(id):
    conv = model.Conversation.query.get_or_404(id)
    user = get_current_user()
    last_message_id = int(request.args.get('last_message_id', -1, type=int))
    messages = conv.get_updated_messages(last_message_id, user)
    last_message_id = messages[-1].id if messages else last_message_id
    conv.mark_read(user)
    # FIXME: for some reason the Conversation object goes away after commit
    result = utils.jsonify(
        conversation=conv,
        messages=messages, 
        last_message_id=last_message_id
    )
    db.session.commit()
    return result

@app.route('/conversations/<int:id>/post', methods=['POST'])
def post_message(id):
    user = get_current_user()
    conv = model.Conversation.query.get_or_404(id)
    text = request.form['text']
    if not text.strip():
        abort(400)
    if (conv.owner != user and conv.status == model.Conversation.STATUS.PENDING):
        conv.status = model.Conversation.STATUS.ACTIVE
    conv.mark_read(user)
    message = model.Message(user, escape(request.form['text']))
    conv.messages.append(message)
    conv.update_time = datetime.utcnow()
    db.session.commit()

    send_email_updates(conv, message, user)

    return 'OK', 201

@app.route('/conversations/new', methods=['GET', 'POST'])
def new_conversation_yes():
    return new_conversation('new_conversation.html')

@app.route('/conversations/new_notyet', methods=['GET', 'POST'])
def new_conversation_notyet():
    return new_conversation('new_conversation_notyet.html')

def new_conversation(template):
    user = get_current_user()

    if request.method == 'GET':
        return render_template(template)

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['message']
        if not title or not text:
            abort(400)
        conv = model.Conversation(user, request.form['title'])
        conv.messages.append(model.Message(user, escape(request.form['message'])))
        db.session.commit()
        return redirect(url_for('conversation', id=conv.id), code=303)

@app.route('/settings')
# FIXME: replace forms with Flask-WTF or better
def settings():
    user = get_current_user()
    return render_template('settings.html')

@app.route('/register', methods=['GET', 'POST'])
# FIXME: replace forms with Flask-WTF or better
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password2 = request.form['password2']
        if not name:
            return redirect(url_for('register', error='no_name', goto=request.args.get('goto')))
        if not password:
            return redirect(url_for('register', error='no_password', name=name, goto=request.args.get('goto')))
        if not password2:
            return redirect(url_for('register', error='no_password2', name=name, goto=request.args.get('goto')))
        existing = model.User.query.filter_by(name=name).first()
        if existing:
            return redirect(url_for('register', error='user_exists', name=existing.name, goto=request.args.get('goto')))
        if password != password2:
            return redirect(url_for('register', error='password_mismatch', name=name, goto=request.args.get('goto')))

        user = model.User(name, password.encode('utf8'))
        db.session.add(user)
        db.session.commit()

        session['logged_in_user'] = name
        return redirect(urldecode(request.args.get('goto', '')) or url_for('main'), code=303)
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if not name:
            return redirect(url_for('login', error='no_name', goto=request.args.get('goto')))
        if not password:
            return redirect(url_for('login', error='no_password', name=name, goto=request.args.get('goto')))
        user = model.User.query.filter_by(name=name).first()
        if not user:
            return redirect(url_for('login', error='bad_password', name=name, goto=request.args.get('goto')))
        password_hash = utils.encrypt_password(password, name)
        if user.password_hash != password_hash:
            return redirect(url_for('login', error='bad_password', name=name, goto=request.args.get('goto')))
        session['logged_in_user'] = request.form['name']
        return redirect(urldecode(request.args.get('goto') or '') or url_for('main'), code=303)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    user = get_current_user()
    session['logged_in_user'] = None
    return redirect(urldecode(request.args.get('goto')) or url_for('main'))

@app.template_filter('urlencode')
def urlencode_filter(s):
    if isinstance(s, unicode):
        s = s.encode('utf8')
    return Markup(urllib.quote_plus(s))

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

def detect_user_message_type(conversation):
    if session.get('logged_in_user') == conversation.owner.name:
        return model.Message.TYPE.TALKER
    else:
        return model.Message.TYPE.LISTENER

def get_current_user(required=True):
    if session.get('logged_in_user'):
        user = model.User.get_current()
        if user:
            return user
        else:
            abort(403)
    if required:
        abort(403)

def send_email_updates(conversation, message, author):
    # FIXME: move the actual sending to a worker behind a queue
    try:
        body = render_template('email_update.html',
            conversation=conversation,
            message=message,
            author=author
        )
        mail = postmark.PMMail(
            api_key=app.config['POSTMARK_API_KEY'],
            sender='info@openemotion.org', 
            to='eli.finer@gmail.com', 
            subject='[openemotion] %s' % conversation.title,
            html_body=body
        )
        mail.send()
    except:
        import traceback
        traceback.print_exc()

@app.errorhandler(403)
def page_not_found(e):
    return redirect(url_for('login', goto=request.path))

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
