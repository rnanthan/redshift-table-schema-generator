from common.log_util import log
from common.redshift_util import RedshiftDataManager
from common.config import dbHost, dbName, dbUser, dbPassword


def execute_data_transformer():
    try:
        dbCon = RedshiftDataManager.get_conn(dbHost, dbUser, dbPassword, dbName)
        script = open('output/create_table.sql', "r").read()
        log.debug(f'Transformation Script: {script}')
        log.info('Start creating table.')
        RedshiftDataManager.execute_update(dbCon, script)
        log.info('Finish creating table.')
    except Exception as e:
        log.error('Error in creating table. {0}'.format(e))


if __name__ == '__main__':
    execute_data_transformer()