# coding=utf-8
"""
MSSQL Hanlders
"""
from app.core.db.backends.base import BaseEngine


class MSSQLPyODBC(BaseEngine):
    """
    Engine connects to MS SQL Server via PyODBC driver
    """

    def make_connection_string(self):
        """
        Make connection string
        :return:
        """
        connection_str = 'mssql+pyodbc://{username}:{password}@{host}:{port}/{name}' \
                         '?driver={driver}'.format(username=self.config.get('USERNAME', ''),
                                                   password=self.config.get('PASSWORD', ''),
                                                   host=self.config.get('HOST', '127.0.0.1'),
                                                   port=self.config.get('PORT', '1433'),
                                                   name=self.config.get('NAME', ''),
                                                   driver=self.config.get('DRIVER', 'FreeTDS'))
        return connection_str
