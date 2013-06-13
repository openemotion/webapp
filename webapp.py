import os
import sys
import logging
from datetime import datetime

import flask
import utils

app = flask.Flask(__name__)
app.config.from_object(os.environ.get('OPENEM_CONFIG', 'config.dev'))
app.logger.addHandler(logging.StreamHandler(sys.stdout))

import model
db = model.db
db.init_app(app)

@app.route('/')
def main():
    conversations = model.Conversation.query.filter_by(is_example=True).order_by(model.Conversation.update_time.desc()).all()
    return flask.render_template('landing.html', conversations=conversations)

@app.route('/faq')
def faq():
    return flask.render_template('faq.html')

@app.route('/terms')
def terms():
    return flask.render_template('terms.html')

@app.route('/conversations/<int:id>/')
@app.route('/conversations/<int:id>/<slug>')
def conversation(id, slug=None):
    conv = model.Conversation.query.get_or_404(id)
    if slug != conv.slug:
        return flask.redirect(flask.url_for('conversation', id=id, slug=conv.slug, **flask.request.args))

    # if author supplied in the URL, store it in session and redirect to a URL without it
    if 'author' in flask.request.args:
        flask.session['conversation_%d_author_id' % conv.id] = flask.request.args.get('author', None)
        return flask.redirect(flask.url_for('conversation', id=id, slug=conv.slug))

    author = get_current_author(conv, allow_none=True)
    new_message_type = model.Message.TYPE.TALKER if conv.owner is author else model.Message.TYPE.LISTENER
    return flask.render_template(
        'conversation.html', 
        conversation=conv, 
        messages=list(conv.messages), 
        author=author,
        new_message_type=new_message_type
    )

@app.route('/conversations/<int:id>/join', methods=['POST'])
def join_conversation(id, slug=None):
    conv = model.Conversation.query.get_or_404(id)
    name = flask.request.form['name'].strip()
    if not name:
        flask.abort(400)
    author = model.Author(name)
    conv.authors.append(author)
    db.session.commit()
    return flask.redirect(flask.url_for('conversation', id=conv.id, slug=conv.slug, author=author.id), code=303)

@app.route('/conversations/<int:id>/updates')
def conversation_updates(id):
    conv = model.Conversation.query.get_or_404(id)
    author = get_current_author(conv)
    last_message_id = int(flask.request.args.get('last_message_id', -1, type=int))
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
    print flask.request.form['author']
    conv = model.Conversation.query.get_or_404(id)
    author = get_current_author(conv)
    text = flask.request.form['text']
    if not text.strip():
        flask.abort(400)
    if (conv.owner != author and conv.status == model.Conversation.STATUS.PENDING):
        conv.status = model.Conversation.STATUS.ACTIVE
    conv.messages.append(model.Message(author, flask.escape(flask.request.form['text'])))
    conv.update_time = datetime.utcnow()
    db.session.commit()
    return 'OK', 201

@app.route('/conversations/new', methods=['GET', 'POST'])
def new_conversation():
    if flask.request.method == 'GET':
        return flask.render_template('new_conversation.html')

    if flask.request.method == 'POST':
        title = flask.request.form['title']
        text = flask.request.form['message']
        author = flask.request.form['author']
        if not title or not text or not author:
            flask.abort(400)

        conv = model.Conversation(flask.request.form['title'])
        author = model.Author(flask.request.form['author'], is_owner=True)
        conv.authors.append(author)
        conv.messages.append(model.Message(author, flask.escape(flask.request.form['message'])))
        db.session.add(conv)
        db.session.commit()
        return flask.redirect(flask.url_for('conversation', id=conv.id, slug=conv.slug, author=author.id), code=303)

@app.route('/conversations/all')
def all():
    conversations = model.Conversation.query.order_by(model.Conversation.update_time.desc()).all()
    return flask.render_template('all.html', conversations=conversations)

def include_raw(filename):
    return flask.Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])
app.jinja_env.globals.update(include_raw=include_raw)

def get_current_author(conv, allow_none=False):
    author_id = flask.session.get('conversation_%d_author_id' % conv.id, None)
    author = model.Author.query.get(author_id) if author_id else None
    if not allow_none:
        if not author:
            flask.abort(403)
    if author and author.conversation is not conv:
        flask.abort(403)
    return author

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
