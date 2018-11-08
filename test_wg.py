import random
import sqlite3
import json
import logging
from random import randrange




db_scheme = {
    'hulls': ('armor', 'type', 'engine'),
    'weapons': ('reload speed', 'rotational speed', 'diameter', 'power volley', 'count'),
    'engines': ('power', 'type')
}


class MixParametrs:

    DUMP_FILENAME = 'dump.json'

    def __init__(self):

        self.dump_dict = {
            'ships': {},
            'weapons': {},
            'hulls': {},
            'engines': {}
        }


    def dump_data_base(self):

        conn = sqlite3.connect("Wargaming.db")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ships")

        for row in cursor:
            self.dump_dict['ships'][row['ship']] = {
                    'weapon': row['weapon'],
                    'hull': row['hull'],
                    'engine': row['engine']
                }

        cursor.execute("SELECT * FROM weapons")
        for row in cursor:
            self.dump_dict['weapons'][row['weapon']] = {
                    'reload speed': row['reload speed'],
                    'rotational speed': row['rotational speed'],
                    'diameter': row['diameter'],
                    'power volley': row['power volley'],
                    'count': row['count']
                }

        cursor.execute("SELECT * FROM hulls")
        for row in cursor:
            self.dump_dict['hulls'][row['hull']] = {
                    'armor': row['armor'],
                    'type': row['type'],
                    'engine': row['capacity']
                }

        cursor.execute("SELECT * FROM engines")
        for row in cursor:
            self.dump_dict['engines'][row['engine']] = {
                    'power': row['power'],
                    'type': row['type']
                }

        with open(self.DUMP_FILENAME, 'w') as file:
            logging.info('Write logs to file: "{}"'.format(self.DUMP_FILENAME))
            dump_json = json.dumps(self.dump_dict, indent=2)
            logging.debug('Writing JSON:\n{}'.format(dump_json))
            file.write(dump_json)

        return self.dump_dict

    def ships_random(self):
        conn = sqlite3.connect("Wargaming.db")
        cursor = conn.cursor()
        for index in range(1, 201):
            req = ("UPDATE Ships SET 'weapon' = ?, 'hull'= ?,'engine'= ? WHERE ship= ? ")
            cursor.execute(req, ('weapon-{}'.format(random.randint(1, 20)), 'hull-{}'.format(random.randint(1, 5)),
                                 'engine-{}'.format(random.randint(1, 6)), 'ship-{}'.format(index)))
            conn.commit()

    def params_weapons(self):
        conn = sqlite3.connect("Wargaming.db")
        cursor = conn.cursor()
        number_params = random.randint(1, 3)
        list_params = []
        while len(list_params) < number_params:
            random_item = db_scheme['weapons'][randrange(number_params)]
            if random_item not in list_params:
                list_params.append(random_item)
        for index in range(1, 21):
            values = [random.randint(1, 100) for i in range(number_params)]
            request_data = []
            for i in range(number_params):
                request_data.append('"{}"={}'.format(list_params[i], values[i]))
            req = 'UPDATE weapons SET {} WHERE weapon="{}"'.format(', '.join(request_data), 'weapon-{}'.format(index))
            logging.debug(req)
            cursor.execute(req)
            conn.commit()

    def params_hulls(self):
        conn = sqlite3.connect("Wargaming.db")
        cursor = conn.cursor()
        number_params = random.randint(1, 2)
        list_params = []
        while len(list_params) < number_params:
            random_item = db_scheme['hulls'][randrange(number_params)]
            if random_item not in list_params:
                list_params.append(random_item)
        for index in range(1, 6):
            values = [random.randint(1, 100) for i in range(number_params)]
            request_data = []
            for i in range(number_params):
                request_data.append('"{}"={}'.format(list_params[i], values[i]))
            req = 'UPDATE hulls SET {} WHERE hull="{}"'.format(', '.join(request_data), 'hull-{}'.format(index))
            logging.debug(req)
            cursor.execute(req)
            conn.commit()

    def params_engines(self):
        conn = sqlite3.connect("Wargaming.db")
        cursor = conn.cursor()
        number_params = random.randint(1, 1)
        list_params = []
        while len(list_params) < number_params:
            random_item = db_scheme['engines'][randrange(number_params)]
            if random_item not in list_params:
                list_params.append(random_item)
        for index in range(1, 7):
            values = [random.randint(1, 100) for i in range(number_params)]
            request_data = []
            for i in range(number_params):
                request_data.append('"{}"={}'.format(list_params[i], values[i]))
            req = 'UPDATE engines SET {} WHERE engine="{}"'.format(', '.join(request_data), 'engine-{}'.format(index))
            logging.debug(req)
            cursor.execute(req)
            conn.commit()
def setup():
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s [%(asctime)s] %(message)s')
    logging.info('tests setup')
    qw = MixParametrs()
    qw.dump_data_base()
    qw.params_weapons()
    qw.params_engines()
    qw.params_hulls()
    qw.ships_random()


def test_weapons():
    conn = sqlite3.connect("Wargaming.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT Ships.ship,
                             weapons.weapon,
                             weapons.diameter,
                             weapons.'power volley',
                             weapons.'rotational speed',
                             weapons.'reload speed',
                             weapons.'count'
                      FROM Ships INNER JOIN weapons
                      ON ships.weapon=weapons.weapon''')
    for row in cursor:
        data = {
            'ship': row['ship'],
            'weapon': row['weapon'],
            'reload speed': row['reload speed'],
            'rotational speed': row['rotational speed'],
            'diameter': row['diameter'],
            'power volley': row['power volley'],
            'count': row['count']
        }
        yield check_weapons, data
        yield check_weapons_params, data


def test_hulls():
    conn = sqlite3.connect("Wargaming.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT Ships.ship,
                             hulls.'hull',
                             hulls.'armor',
                             hulls.'type',
                             hulls.'capacity'
                      FROM Ships INNER JOIN hulls
                      ON ships.hull=hulls.hull''')
    for row in cursor:
        data = {
            'ship': row['ship'],
            'hull': row['hull'],
            'armor': row['armor'],
            'type': row['type'],
            'capacity': row['capacity']
        }
        yield check_hulls, data
        yield check_hulls_params, data


def test_engines():
    conn = sqlite3.connect("Wargaming.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT Ships.ship,
                             engines.'engine',
                             engines.'power',
                             engines.'type'
                     FROM Ships INNER JOIN engines
                     ON ships.engine=engines.engine''')
    for row in cursor:
        data = {
            'ship': row['ship'],
            'engine': row['engine'],
            'power': row['power'],
            'type': row['type']
        }

        yield check_engines, data
        yield check_engines_params, data


def check_engines(data):
    with open("dump.json", 'r') as file:
        dump_text = file.read()
        dump_json = json.loads(dump_text)
    output_header = '{}, {}'.format(data['ship'], data['engine'])
    expected_weapon = dump_json['ships'][data['ship']]['engine']
    assert data['engine'] == expected_weapon, '{}\n\texpected {}, was {}'.format(output_header, expected_weapon,
                                                                                 data['engine'])


def check_engines_params(data):
    with open("dump.json", 'r') as file:
        dump_text = file.read()
        dump_json = json.loads(dump_text)
    output_header = '{}, {}'.format(data['ship'], data['engine'])
    unexpected_values = []
    for item in data:
        expected_engine = dump_json['engines'][data['engine']]
        if item in expected_engine and data[item] != expected_engine[item]:
            unexpected_values.append('{}: expected {}, was {}'.format(item, expected_engine[item], data[item]))
    unexpected_output = '\n\t'.join(unexpected_values)
    assert not unexpected_values, '{}\n\t{}'.format(output_header, unexpected_output)


def check_weapons(data):
    with open("dump.json", 'r') as file:
        dump_text = file.read()
        dump_json = json.loads(dump_text)
    output = '{}, {}\n\texpected {}, was {}'
    dump_weapon = dump_json['ships'][data['ship']]['weapon']
    assert data['weapon'] == dump_weapon, output.format(data['ship'], data['weapon'], dump_weapon, data['weapon'])


def check_weapons_params(data):
    with open("dump.json", 'r') as file:
        dump_text = file.read()
        dump_json = json.loads(dump_text)
    output_header = '{}, {}'.format(data['ship'], data['weapon'])
    unexpected_values = []
    for item in data:
        expected_engine = dump_json['weapons'][data['weapon']]
        if item in expected_engine and data[item] != expected_engine[item]:
            unexpected_values.append('{}: expected {}, was {}'.format(item, expected_engine[item], data[item]))
    unexpected_output = '\n\t'.join(unexpected_values)
    assert not unexpected_values, '{}\n\t{}'.format(output_header, unexpected_output)


def check_hulls(data):
    with open("dump.json", 'r') as file:
        dump_text = file.read()
        dump_json = json.loads(dump_text)
    output = '{}, {}\n\texpected {}, was {}'
    dump_weapon = dump_json['ships'][data['ship']]['hull']
    assert data['hull'] == dump_weapon, output.format(data['ship'], data['hull'], dump_weapon, data['hull'])


def check_hulls_params(data):
    with open("dump.json", 'r') as file:
        dump_text = file.read()
        dump_json = json.loads(dump_text)
    output_header = '{}, {}'.format(data['ship'], data['hull'])
    unexpected_values = []
    for item in data:
        expected_engine = dump_json['hulls'][data['hull']]
        if item in expected_engine and data[item] != expected_engine[item]:
            unexpected_values.append('{}: expected {}, was {}'.format(item, expected_engine[item], data[item]))
    unexpected_output = '\n\t'.join(unexpected_values)
    assert not unexpected_values, '{}\n\t{}'.format(output_header, unexpected_output)
