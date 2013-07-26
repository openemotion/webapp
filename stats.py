import os
import sys
import psycopg2

class Connection(object):
    def __init__(self, credentials):
        self.conn = psycopg2.connect(credentials).cursor()

    def query(self, sql):
        self.conn.execute(sql)
        return self.conn.fetchall()

    def count(self, table):
        return self.query("select count(*) from %s;" % table)[0][0]

def log(msg):
    print >>sys.stderr, msg

def main():
    log('connecting...')
    credentials = os.popen('heroku pg:credentials --app openemotion DATABASE_URL').readlines()[1].strip(' \n"')
    conn = Connection(credentials)
    log('fetching...')

    print
    print 'Total'
    print '-----'
    print '%d users' % conn.count('users')
    print '%d conversations' % conn.count('conversations')
    print '%d messages' % conn.count('messages')

    print
    print 'Messages Last 7 days'
    print '--------------------'
    sql = """
    select date_trunc('day', post_time), count(*)
    from messages 
    where post_time >= current_date - interval '7 days'
    group by date_trunc('day', post_time)
    order by date_trunc('day', post_time)
    """
    for date, count in conn.query(sql):
        print '%s: %d messages' % (date.strftime('%Y/%m/%d %a'), count)

    print
    print 'Users Last 7 days'
    print '-----------------'
    sql = """
    select date_trunc('day', create_time), count(*)
    from users
    where create_time >= current_date - interval '7 days'
    group by date_trunc('day', create_time)
    order by date_trunc('day', create_time)
    """
    for date, count in conn.query(sql):
        print '%s: %d new users' % (date.strftime('%Y/%m/%d %a'), count)

if __name__ == '__main__':
    main()