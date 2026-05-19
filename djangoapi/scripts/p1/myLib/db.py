# djangoapi/scripts/p1/myLib/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from myLib import p1Settings as settings

class Db:
    def __init__(self, autoCommit=True, getRowsAsDicts=True):
        self.autoCommit = autoCommit
        self.getRowsAsDicts = getRowsAsDicts
        self.conn = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT
        )
        if self.getRowsAsDicts:
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        else:
            self.cursor = self.conn.cursor()
        self.result = None

    def query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if self.autoCommit:
                self.conn.commit()
            
            # Guardamos los resultados dependiendo de la query
            if "insert" in query.lower() or "select" in query.lower():
                self.result = self.cursor.fetchall()
            else:
                self.result = self.cursor.rowcount
            return True, "Query OK"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)

    def disconnect(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass