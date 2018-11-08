#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import random
import os


class GenerateData():

    def __init__(self, path_db):
        CREATING_REQ = """BEGIN TRANSACTION;
                          CREATE TABLE `Ships` (
                            `ship` TEXT, `weapon` TEXT, `hull` TEXT, `engine` TEXT,
                            PRIMARY KEY(`ship`),
                            FOREIGN KEY (weapon) REFERENCES weapons(weapon),
                            FOREIGN KEY (hull)   REFERENCES hulls(hull),
                             FOREIGN KEY (engine) REFERENCES engines(engine));
                          CREATE TABLE `engines` (
                            `engine` TEXT, `power` INTEGER, `type` INTEGER, PRIMARY KEY(`engine`));
                          CREATE TABLE `hulls` (`hull` TEXT, `armor` INTEGER, `type` INTEGER, `capacity` INTEGER, PRIMARY KEY(`hull`));
                        CREATE TABLE "weapons" (
                        `weapon` TEXT,
                        `reload speed` INTEGER,
                        `rotational speed` INTEGER,
                        `diameter` INTEGER,
                        `power volley` INTEGER,
                        `count` INTEGER,
                        PRIMARY KEY(`weapon`)
                        );
                            COMMIT;"""
        self.path_db = path_db
        self.conn = sqlite3.connect(self.path_db)
        self.cursor = self.conn.cursor()
        self.cursor.executescript(CREATING_REQ)
        self.conn.commit()


    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def generate_ships(self):
        for index in range(1, 201):
            self.cursor.execute("SELECT weapon FROM weapons ORDER BY RANDOM() LIMIT 1")
            weapon = self.cursor.fetchone()
            self.cursor.execute("SELECT hull FROM hulls ORDER BY RANDOM() LIMIT 1")
            hull = self.cursor.fetchone()
            self.cursor.execute("SELECT engine FROM engines ORDER BY RANDOM() LIMIT 1")
            engine = self.cursor.fetchone()
            req = "INSERT INTO Ships ('ship', 'weapon', 'hull','engine') VALUES ('{}', '{}', '{}', '{}')".format(
                'ship-{}'.format(index), weapon[0], hull[0], engine[0])
            self.cursor.execute(req)

    def generate_weapons(self):
        for index in range(1, 21):
            req = "INSERT INTO weapons ('weapon', 'reload speed', 'rotational speed', 'diameter', 'power volley','count') VALUES ('{}', '{}', '{}', '{}','{}','{}')".format(
                'weapon-{}'.format(index), random.randint(1, 101), random.randint(1, 101), random.randint(1, 101),
                random.randint(1, 101), random.randint(1, 101))
            self.cursor.execute(req)

    def generate_hulls(self):
        for index in range(1, 6):
            req = "INSERT INTO hulls ('hull', 'armor', 'type','capacity') VALUES ('{}', '{}', '{}', '{}')".format(
                'hull-{}'.format(index), random.randint(1, 101), random.randint(1, 101), random.randint(1, 101))
            self.cursor.execute(req)

    def generate_engines(self):
        for index in range(1, 7):
            req = "INSERT INTO engines ('engine', 'power', 'type') VALUES ('{}', '{}', '{}')".format(
                'engine-{}'.format(index), random.randint(1, 101), random.randint(1, 101))
            self.cursor.execute(req)


if __name__ == '__main__':
    DB_FILENAME = 'Wargaming.db'
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, DB_FILENAME)
    if not os.path.exists(path_db):
        filling_table = GenerateData(path_db)
        filling_table.generate_weapons()
        filling_table.generate_hulls()
        filling_table.generate_engines()
        filling_table.generate_ships()
        filling_table.commit_and_close()
    else:
        print('Already exist: "{}"'.format(path_db))
