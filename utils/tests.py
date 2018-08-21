from sqlalchemy import event
from sqlalchemy.engine import Connection


class QueriesCounter:

    def __init__(self, print_sql=False):
        self.conn = Connection
        self.count = 0
        self.print_sql = print_sql
        event.listen(self.conn, 'before_cursor_execute', self.callback)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        event.remove(self.conn, 'before_cursor_execute', self.callback)

    def callback(self, conn, cursor, statement,
                 parameters, context, executemany):
        self.count += 1
        if self.count > 0 and self.print_sql:
            print(statement, "\n")

    def reset(self):
        self.count = 0
