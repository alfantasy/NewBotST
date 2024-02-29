import sqlite3
from lib.items import items
from lib.price import items

conn = sqlite3.connect('stalker_game.db')
cursor = conn.cursor()

class PlayerInventory:
    prices = {1: 1000, 2: 2000, 3: 3000, 4: 4000, 5: 5000, 6: 6000, 7: 7000, 8: 8000, 9: 9000, 10: 10000, 11: 11000, 12: 12000, 13: 13000, 14: 14000, 15: 15000, 16: 16000, 17: 17000, 18: 18000, 19: 19000, 20: 20000, 21: 21000, 22: 22000, 23: 23000, 24: 24000, 25: 25000, 26: 26000, 27: 27000}
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
        result = ''
        cursor.execute('SELECT id, quantity FROM inventory WHERE (user_id = ? AND item_id = ?) ', (player_id, item_id))
        row = cursor.fetchall()
        temp_id = row[0][0]
        temp_quantity = row[0][1]
        if int(temp_quantity) > 1:
            temp_quantity -= 1
        if row and int(row[0][1]) > 1:
            cursor.execute('UPDATE inventory SET quantity = ? WHERE (id = ? AND user_id = ? AND item_id = ?)', (temp_quantity, temp_id, player_id, item_id))
            print(f'Количество предмета {items[int(item_id)]} было уменьшено у игрока с ID {player_id}')
            result = f"Вы выбросили одну единицу предмета {items[int(item_id)]}"
        elif row and int(row[0][1]) == 1:
            cursor.execute("DELETE FROM inventory WHERE id = ? AND item_id = ?", (temp_id, item_id)) 
            conn.commit()
            print(f'Предмет {items[int(item_id)]} у игрока с ID {player_id} удален')
            result = f'Вы выбросили предмет {items[int(item_id)]}'
        else:
            result = f'Указанного Вами предмета нет в Вашем инвентаре.'
        return result

    async def add_money_to_player(self, player_id, amount):
        player = await player.get(player_id)
        player.money += amount
        await player.save()



    # def update_quantity(self, player_id, item_id, new_quantity):
    #     if item_id in armor or item_id in weapons or item_id in detectors or item_id in items or item_id in artifacts:
    #         cursor.execute("UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_id = ?", (new_quantity, player_id, item_id))
    #         conn.commit()
    #         print('Предмет обновлен')

    def get_inventory(self, player_id):
        cursor.execute("SELECT item_id, quantity FROM inventory WHERE user_id = ?", (player_id,))
        inventory = cursor.fetchall()
        return inventory
    

   


    def buy_item(self, player_id, item_id):
        if item_id in self.prices:  # Проверяем, что предмет есть в словаре с ценами
            item_cost = self.prices[item_id]
            player_balance = self.get_player_money(player_id)  # Получаем баланс игрока
            if player_balance >= item_cost:  # Проверяем достаточность средств у игрока
                self.update_player_money(player_id, player_balance - item_cost)  # Обновляем баланс игрока
                self.add_item_to_inventory(player_id, item_id)  # Добавляем предмет в инвентарь
                return f'Вы купили предмет {item_id} за {item_cost}'
            else:
                return 'Недостаточно средств для покупки'
        else:
            return 'Такого предмета нет в магазине'

    def sell_item(self, player_id, item_id):
        inventory = self.get_inventory(player_id)
        for inv_item_id, _ in inventory:
            if item_id == inv_item_id:
                item_cost = self.prices[item_id]
                self.remove_item_from_inventory(player_id, item_id)  # Удаляем предмет из инвентаря
                self.update_player_money(player_id, self.get_player_money(player_id) + item_cost)  # Увеличиваем баланс игрока
                return f'Вы продали предмет {item_id} за {item_cost}'
        return 'У вас нет такого предмета в инвентаре'