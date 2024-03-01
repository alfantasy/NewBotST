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
        cursor.execute('SELECT money, item_id FROM user_stats, inventory(money = ? AND item_id=? AND user_id=?)', (player_id, item_id))
        if item_id in items:  
            cursor.execute('UPDATE money=?, item_id FROM user_stats, inventory WHERE(user_id=? AND money=? AND item_id=?)', (player_id, item_id))
            item_cost = items[item_id]['price']  
            player_balance = self.get_money(player_id)  
            if player_balance >= item_cost:  
                self.update_player_money(player_id, player_balance - item_cost)  
                self.add_item_to_inventory(player_id, item_id)  
                return f'Вы купили предмет {items[item_id]["name"]} за {item_cost}'
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




class user_wallet:
    def add_money(self, user_id, money):
        user_stats = money
        money = self.add_money(user_id)
        cursor.execute('SELECT money FROM user_stats WHERE (user_id=? AND money=?)', (user_id, money))
        row = row.fetchall()
        if row:
             print(row[0][0])
             print(row[0])
             temp_id = row[0][0]
             temp_quantity = 0
             temp_quantity += row[0][1] + 1
             cursor.execute("UPDATE money SET quantity = ? WHERE (user_id = ? AND money = ?)", (temp_quantity, temp_id, user_id, money))
             print(f'Количество монет {[int(money)]} у игрока с ID {user_id} изменено')
             result = f'Количество монет {[int(money)]} изменено.'
        conn.commit()

        
    
 
            
     
   