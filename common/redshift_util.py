import psycopg2
from common.log_util import log


class RedshiftDataManager(object):

    @staticmethod
    def execute_update(con, script):
        log.debug('script : {0}'.format(script))
        try:
            cur = con.cursor()
            cur.execute(script)
            con.commit()
            log.info('changed committed. {0}'.format(con))
            result = True
        except Exception as e:
            log.error('Error in data update. {0}'.format(e))
            con.rollback()
            result = False
        finally:
            log.info('closing connection.{0}'.format(con))
            cur.close()
            con.close()
            log.info('connection closed.{0}'.format(con))
        return result

    @staticmethod
    def get_conn(host, user, password, database):
        return psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            sslmode='require'
        )
