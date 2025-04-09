import asyncio
import asyncpg
import sys
import time

async def check_db():
    retries = 30
    while retries > 0:
        try:
            # подключение к базе данных по умолчанию
            conn = await asyncpg.connect(
                user='postgres',
                password='12345678',
                database='postgres',
                host='db'
            )
            
            # Проверка, существует ли тестовая база данных
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1",
                'test_wallet_db'
            )
            
            if not exists:
                # Создает тестовую базу данных, если она не существует
                await conn.execute('CREATE DATABASE test_wallet_db')
                print("Created test_wallet_db database")
            
            await conn.close()
            
            # Тестовое подключение к тестовой базе данных
            test_conn = await asyncpg.connect(
                user='postgres',
                password='12345678',
                database='test_wallet_db',
                host='db'
            )
            await test_conn.close()
            
            print("Database is ready!")
            return True
        except Exception as e:
            print(f"Database not ready yet: {e}")
            retries -= 1
            await asyncio.sleep(1)
    return False

if __name__ == "__main__":
    if not asyncio.run(check_db()):
        sys.exit(1)
