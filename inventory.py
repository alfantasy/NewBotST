import sqlite3
from lib.items import items

conn = sqlite3.connect('stalker_game.db')
cursor = conn.cursor()

class PlayerInventory:
    def add_item_up_quanity(self, player_id, item_id, quantity):
        result = ''
        cursor.execute('SELECT user_id FROM inventory WHERE (user_id = ? AND item_id = 0)', (player_id,))
        row = cursor.fetchall()
        cursor.execute('SELECT id, quantity FROM inventory WHERE (user_id = ? AND item_id = ?)', (player_id, item_id))
        row0 = cursor.fetchall()
        if row0:
            print(row0[0][0])
            print(row0[0])
            temp_id = row0[0][0]
            temp_quantity = 0
            temp_quantity += row0[0][1] + 1
            cursor.execute("UPDATE inventory SET quantity = ? WHERE (id = ? AND user_id = ? AND item_id = ?)", (temp_quantity, temp_id, player_id, item_id))
            print(f'Количество {items[int(item_id)]} у игрока с ID {player_id} обновлен')
            result = f'Количество предмета {items[int(item_id)]} изменено.'
        else:
            if row:
                cursor.execute("UPDATE inventory SET item_id = ?, quantity = ? WHERE user_id = ?", (item_id, quantity, player_id))
                print(f'Предмет добавлен у ID {player_id}')
                result = f'В Ваш инвентарь добавился {items[int(item_id)]}'
            else:
                cursor.execute("INSERT INTO inventory (user_id, item_id, quantity) VALUES (?, ?, ?)", (player_id, item_id, quantity))
                print(f'Предмет добавлен у ID {player_id}')
                result = f'В Ваш инвентарь добавился {items[int(item_id)]}'
        conn.commit()
        return result

    def remove_item(self, player_id, item_id):
        cursor.execute("DELETE FROM inventory WHERE user_id = ? AND item_id = ?", (player_id, item_id))
        conn.commit()
        print('Предмет удален')

    # def update_quantity(self, player_id, item_id, new_quantity):
    #     if item_id in armor or item_id in weapons or item_id in detectors or item_id in items or item_id in artifacts:
    #         cursor.execute("UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_id = ?", (new_quantity, player_id, item_id))
    #         conn.commit()
    #         print('Предмет обновлен')

    def get_inventory(self, player_id):
        cursor.execute("SELECT item_id, quantity FROM inventory WHERE user_id = ?", (player_id,))
        inventory = cursor.fetchall()
        return inventory
    
