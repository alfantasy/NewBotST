import sqlite3
from lib.items import *

class PlayerInventory:
    def __init__(self):
        self.conn = sqlite3.connect('stalker_game.db')
        self.cursor = self.conn.cursor()

    def add_item(self, player_id, item_id, quantity):
        if item_id in armor.keys() or item_id in weapons.keys() or item_id in detectors.keys() or item_id in items.keys() or item_id in artifacts.keys():
            self.cursor.execute("INSERT INTO inventory (user_id, item_id, quantity) VALUES (?, ?, ?)", (player_id, item_id, quantity))
            self.conn.commit()
            print('Предмет добавлен')

    def remove_item(self, player_id, item_id):
        if item_id in armor or item_id in weapons or item_id in detectors or item_id in items or item_id in artifacts:
            self.cursor.execute("DELETE FROM inventory WHERE user_id = ? AND item_id = ?", (player_id, item_id))
            self.conn.commit()
            print('Предмет удален')

    def update_quantity(self, player_id, item_id, new_quantity):
        if item_id in armor or item_id in weapons or item_id in detectors or item_id in items or item_id in artifacts:
            self.cursor.execute("UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_id = ?", (new_quantity, player_id, item_id))
            self.conn.commit()
            print('Предмет обновлен')

    def get_inventory(self, player_id):
        self.cursor.execute("SELECT item_id, quantity FROM inventory WHERE user_id = ?", (player_id,))
        inventory = self.cursor.fetchall()
        return inventory