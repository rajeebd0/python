import MySQLdb

class DBC(object):

    _instance = None
    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(DBC, self).__new__(
                                self, *args, **kwargs)
        return self._instance

    def connect(self, dsn):
        try:
            self.db_connection = MySQLdb.connect(
                host=dsn['hostname'],
                user=dsn['username'],
                passwd=dsn['password'],
                db=dsn['database'])

        except MySQLdb.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %(e.args[0], e.args[1]))

    def read_data(self, table, where = 1):
        x = self.db_connection.cursor()
        sql = "select * from %s " % table
        x.execute(sql)
        rows = x.fetchall()
        for row in rows:
            print row
        return

    def insert_data(self, table, data):
        col = '\',\''.join(data.keys())        
        col = col.replace("'", "`")   
        sql = "INSERT INTO %s (`%s`) VALUES %s " % (table, col, tuple(data.values()))            
        x = self.db_connection.cursor()                                                            
        x.execute(sql)
        self.db_connection.commit()
        return

    def update_data(self,table, data, where = 1):
        col = ''
        whr = ''
        for k, v in data.items():
            temp = "`"+k+"` = "+"'"+v+"'"
            col += " ,"+temp if col else temp
        for k, v in where.items():
            temp = "`"+k+"` = "+"'"+v+"'"
            whr += " ,"+temp if whr else temp
        sql = "UPDATE `%s` SET %s WHERE %s " % (table, col, whr)   
        x = self.db_connection.cursor()                                                    
        x.execute(sql)
        self.db_connection.commit()
        return

    def delete_data(self,table, where):
        whr = ''
        for k, v in where.items():
            temp = "`"+k+"` = "+"'"+v+"'"
            whr += " ,"+temp if whr else temp
        sql = "DELETE FROM `%s` WHERE %s " % (table, whr)   
        # print sql 
        # exit()     
        x = self.db_connection.cursor()                                                    
        x.execute(sql)
        self.db_connection.commit()
        return

if __name__ == "__main__":
    dsn = {
    'username': 'root',
    'password': '123456',
    'hostname': 'localhost',
    'database': 'bucketlist'
    }
    a = DBC()
    a.connect(dsn)
    # a.read_data('users')
    # data = {'name':'fffff','username':'gooll@app.com','password':'123456'}
    where = {'id':'15'}
    # a.insert_data('users', data)
    # a.update_data('users', data, where)
    a.delete_data('users', where)