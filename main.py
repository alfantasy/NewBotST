import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
from inventory import PlayerInventory

bot = Bot(token="6616582391:AAEJ7kzVdwvkxB_MQZOs-QuHoNXTU_w3lxQ")
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
# ---- Создание БД ----
conn = sqlite3.connect('stalker_game.db')

cursor = conn.cursor()

# ---- Создание таблицы с полями ----
cursor.execute('''CREATE TABLE IF NOT EXISTS users_stats (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            username TEXT,
            money INTEGER,
            donate TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                item_id INTEGER,
                quantity INTEGER
)''')

player_inventory = PlayerInventory()

## ХУЙХУЙХУЙХУХЙХУЙХУЙХУХЙУХЙУХЙХУЙХУХЙУХЙХуй

conn.commit()
async def close_database(*args):
    print('Закрытие бота и сохранение DB.')
    conn.close()

@dp.message_handler(commands=['item'])
async def add_item(message: types.Message):
    user_id = message.from_user.id 
    args = message.get_args()
    result = player_inventory.add_item_up_quanity(player_id=user_id, item_id=args, quantity=1)
    await message.answer(result)

@dp.message_handler(commands=['inv'])        
async def inventory_get(message: types.Message):
    user_id = message.from_user.id  
    await message.answer(player_inventory.get_inventory(player_id=user_id))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id  # Получение user_id из сообщения
    username = message.from_user.username  # Получение username из сообщения

    # --- Заполнение БД ----
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users_stats WHERE user_id=?', (user_id,))
    row = cursor.fetchall()
    if row:
        await bot.send_message(user_id, f"Уже зарегистрированы.")
    else:
        cursor.execute("INSERT OR REPLACE INTO users_stats (user_id, username, money) VALUES (?, ?, 0)", (user_id, username))
        cursor.execute("INSERT OR REPLACE INTO inventory (user_id, item_id, quantity) VALUES (?, 0, 0)", (user_id,))
        conn.commit()
        print(f"[CTL] В системе зарегистрирован новый пользователь: \nID: {user_id}\nNICK: {username}")
        await bot.send_message(user_id, f"Вы зарегистрированы.")

@dp.message_handler(commands=['resetit'])
async def remove_item(message: types.Message):
    user_id = message.from_user.id 
    args = message.get_args()
    result = player_inventory.remove_item(player_id=user_id, item_id=args)
    await message.answer(result)

@dp.message_handler(commands=['sale'])
async def remove_item(message: types.Message):
    user_id = message.from_user.id 
    args = message.get_args()
    result = player_inventory.remove_item(player_id=user_id, item_id=args)
    await message.answer(result)

@dp.message_handler(commands=['buy'])
async def add_item(message: types.Message):
    user_id = message.from_user.id 
    args = message.get_args()
    result = player_inventory.add_item_up_quanity(player_id=user_id, item_id=args, quantity=1)
    await message.answer(result)

@dp.message_handler(commands=['add_money'])
async def add_money_to_player_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()
    amount = int(args)  # Получаем сумму для добавления
    result = await player_inventory.add_money_to_player(user_id, amount)
    await message.answer(f'Добавлено {amount} монет. Новый баланс: {result.money}')

conn = sqlite3.connect('stalker_game.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users_stats')
rows = cursor.fetchall()
for row in rows:
    print(row)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=close_database)