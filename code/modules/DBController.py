import sqlite3
from datetime import date, datetime, time
from os import path
import subprocess


class DBController:
    def __init__(self, dbtype=''):
        self._dbtype = dbtype
        self._dbname = ''
        self._conn = False
        self._curTable = False
        self._lastQuere = False
        self.expectedTables = ['notes', 'reminders', 'tasks', 'metadata', 'sub_tasks']
        self.tables = []
        self.connect()

# removers

    def removeNotes(self, where):
        self._curs.execute('DELETE from public.notes WHERE {}'.format(str(where)))
    
    def removeRimenders(self, where):
        self._curs.execute('DELETE from public.reminders WHERE {}'.format(str(where)))

    def removeTasks(self, where):
        self._curs.execute('DELETE from public.tasks WHERE {}'.format(str(where)))

    def removeMetadata(self, where):
        self._curs.execute('DELETE from public.metadata WHERE {}'.format(str(where)))

    def removeSubTasks(self, where):
        self._curs.execute('DELETE from public.sub_tasks WHERE {}'.format(str(where)))

# inserters

    def insertNotes(self, data):
        _id = int(self.getMaxId(self._tables[2]) + 1)
        tmp = "INSERT INTO public.notes VALUES(" + str(_id) + "{}-{}-{} {}:{}"
        self._curs.execute(tmp)

    def insertReminders(self, data):
        _id = int(self.getMaxId(self._tables[2]) + 1)
        self._curs.execute("INSERT INTO public.reminders VALUES(DEFAULT, '" + data[0] + "', " + data[1] + ", '" + data[2] + "', " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + ", " + data[7] + ", '{" + data[8] + "}')")

    def insertTasks(self, data):
        _id = int(self.getMaxId(self._tables[2]) + 1)
        self._curs.execute("INSERT INTO public.tasks VALUES(DEFAULT, '" + data[0] + "', " + data[1] + ", '" + data[2] + "', " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + ", " + data[7] + ", '{" + data[8] + "}')")

    def insertMetadata(self, data):
        _id = int(self.getMaxId(self._tables[2]) + 1)
        self._curs.execute("INSERT INTO public.metadata VALUES(DEFAULT, '" + data[0] + "', " + data[1] + ", '" + data[2] + "', " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + ", " + data[7] + ", '{" + data[8] + "}')")

    def insertSubTasks(self, data):
        _id = int(self.getMaxId(self._tables[2]) + 1)
        self._curs.execute("INSERT INTO public.sub_tasks VALUES(DEFAULT, '" + data[0] + "', " + data[1] + ", '" + data[2] + "', " + data[3] + ", " + data[4] + ", " + data[5] + ", " + data[6] + ", " + data[7] + ", '{" + data[8] + "}')")

# updaters

    def updateMeteodata(self, data):
        self._curs.execute("UPDATE public.meteodata_meteodata SET datetime='" + data[0] + "', place=" + str(data[1]) + ", \"placeName\"" + data[2] + "', temperature=" + str(data[3]) + ", wind_way=" + str(data[4]) + ", wind_speed=" + str(data[5]) + ", air_pressure" + str(data[6]) + ", water_pressure" + str(data[7]) + ", weather='{" + data[8] + "}' WHERE id=" + str(data[0]))

# getters

    def getNotes(self, what='id, create_datetime, text, metadata', where=''):
        self._curTable = 0
        tmp = 'SELECT {} FROM public.notes {}'.format(what, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

    def getReminders(self, what='id, create_datetime, reminder_datetime, text, metadata', where=''):
        self._curTable = 1
        tmp = 'SELECT {} FROM public.reminders {}'.format(what, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

    def getTasks(self, what='id, create_datetime, expire_datetime, tasks, stage', where=''):
        self._curTable = 2
        tmp = 'SELECT {} FROM public.tasks {}'.format(what, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

    def getMetadata(self, what='id, name', where=''):
        self._curTable = 2
        tmp = 'SELECT {} FROM public.tasks {}'.format(what, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

    def getSubTasks(self, what='id, create_datetime, expire_datetime, task_id, weight', where=''):
        self._curTable = 2
        tmp = 'SELECT {} FROM public.tasks {}'.format(what, where)
        self._lastQuere = tmp
        self._curs.execute(tmp)
        records = self._refactorRecords(self._curs.fetchall())
        return records

# Additional functions

    def getTableNames(self):
        tables = self._curs.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self._refactorRecords(tables.fetchall())
        return tables

    def getHederLabels(self, table):
        columns = self._curs.execute("SELECT * FROM {}".format(table))
        columns = self._refactorRecords(columns.fetchall())
        return list(columns.keys())

    def getMaxId(self, table):
        if table in self._tables:
            self._curs.execute('SELECT MAX(id) FROM public.{}'.format(table))
        elif isinstance(table, int):
            if table >= 0 and table < len(self._tables):
                self._curs.execute('SELECT MAX(id) FROM public.{}'.format(self._tables[table]))
        else:
            return 0
        records = self._curs.fetchall()
        if records[0][0] is None:
            return 1
        else:
            return int(records[0][0])

    def initialiseDB(self):
        if path.exists(self._dbname):
            self.connect()
            dataBaseTables = []
            for t in self.expectedTables:
                if t not in dataBaseTables:
                    self.createTables(t)
            return True
        else:
            subprocess.call('touch ../files/main.db')
            self.connect()
            for t in self.expectedTables:
                self.createTables(t)

    def createTables(self, tableName):
        if tableName == 'notes':
            sql = "CREATE TABLE IF NOT EXISTS `notes` (`id` bigint PRIMARY KEY, `create_datetime` TIMESTAMP, `text` TEXT, `metadata` TEXT[])"
        elif tableName == 'reminders':
            sql = "CREATE TABLE IF NOT EXISTS `reminders` (`id` bigint PRIMARY KEY, `create_datetime` TIMESTAMP, `reminder_datetime` TIMESTAMP, `text` TEXT, 'metadata' BIGINT[])"
        elif tableName == 'tasks':
            sql = "CREATE TABLE IF NOT EXISTS `tasks` (`id` bigint PRIMARY KEY, `create_datetime` TIMESTAMP, `expire_datetime` TIMESTAMP, `tasks` BIGINT[], 'stage' FLOAT)"
        elif tableName == 'metadata':
            sql = "CREATE TABLE IF NOT EXISTS `metadata` (`id` bigint PRIMARY KEY, 'name' TEXT)"
        elif tableName == 'sub_tasks':
            sql = "CREATE TABLE IF NOT EXISTS `tasks` (`id` bigint PRIMARY KEY, `create_datetime` TIMESTAMP, `expire_datetime` TIMESTAMP, `task_id` BIGINT, 'weight' FLOAT)"
        
        self._curs.execute(sql)

    def _refactorRecords(self, records):
        result = list()
        for row in records:
            result_row = list()
            for key in row.keys():
                if isinstance(row[key], datetime):
                    row[key] = str(element)
                elif isinstance(row[key], str):
                    if row[key].isdigit():
                        row[key] = float(element)
                    else:
                        if row[key][0] == '{':
                            row[key] = element[1: -1]
                        else:
                            row[key] = element
                elif isinstance(row[key], list):
                    row[key] = element[0]
                elif isinstance(row[key], int):
                    row[key] = element
                elif isinstance(row[key], float):
                    row[key] = float(row[key])

    def save(self):
        self._conn.commit()

    def close(self):
        self._conn.commit()
        self._curs.close()
        self._conn.close()
    
    def connect(self, dbname='main.db'):
        self._conn = sqlite3.connect(dbname)
        self._conn.row_factory = sqlite3.Row
        self._curs = self._conn.cursor()

    def __del__(self):
        self.close()