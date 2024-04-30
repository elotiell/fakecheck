import asyncio
from solana.account import Account
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import transfer
from solana.rpc.commitment import Commitment

# Приватные ключи для шести кошельков
private_keys = [
    '5aJvMHqE7XJJrwnhuUn8ZjFmS6iADjC38hNBUojS6P48gfA5M2Fn5Mc25ufAG3MBymk65iJznxw1vaH3fZJgimng',
    'CpwanGoJ1TQ2hXmB3mvdDB1LXYDnCGp1W5uwE3EUhdrNyufovDEmQk2hs92Jm2zMcvwXbPZHcHABMuaPQqKyQzT',
    '5QMUCTiyTCSN6hM3vgRtbTgdaVEATUGKF7J28E6ShvtpbMzp9RiGshQXdyEzgXFCqzT76CyLC68D9d2QEcC6EACX',
    '23QxzgUaFUqVi83kfBHVEQQ3hLW3eAA9ah3Kh5XGN7cTAktnwRLj6WnsteyEyiXaw7YHXKdnsF5ce8axgHnYCL7K',
    '323nxxeQqsS6dVJ9FXcwZ4qCqQiSPA8T6WNdKkDdHatvxT8cV4u3tSMoFoJ2f2KfefggRGy7GmhPQEQAKQEB1RNW',
    '369YKwS4kNRAiUqLE1zDBY9hU29uRMRB92ya94NWBSDuX7MJ2vzNUx6hDdR7EgqsDWeCnL5F463zQkAwvnAwHZe9'
]

# Основной кошелек, куда будут выводиться средства
main_wallet = Account('DEs3HieD68V8AXnhfjMV976sEmiK6ZZuMNm857johWJdGb1sdBtceCaRYNAV821n12z4PAYuxALV3kA2DLywKSC')

# Создаем клиент для взаимодействия с сетью Solana
client = Client("https://api.mainnet-beta.solana.com")

# Функция для получения истории транзакций кошелька
async def get_wallet_transactions(wallet):
    return await client.get_confirmed_signatures_for_address2(wallet.public_key(), commitment=Commitment.FINALIZED)

# Функция для проверки новых транзакций и вывода средств
async def process_transactions(wallet):
    while True:
        transactions = await get_wallet_transactions(wallet)
        for tx in transactions:
            # Проверяем, если транзакция после последнего обработанного блока
            if tx['slot'] > last_processed_block:
                # Обрабатываем транзакцию
                # В этом месте можем выполнить вывод средств
                print(f'Новая транзакция для кошелька {wallet.public_key()}: {tx}')
                # Обновляем последний обработанный блок
                last_processed_block = tx['slot']
        # Ждем некоторое время перед следующей проверкой
        await asyncio.sleep(60)  # Проверяем новые транзакции каждую минуту

# Запускаем асинхронную функцию для каждого кошелька
async def main():
    tasks = []
    for private_key in private_keys:
        wallet = Account(private_key)
        task = asyncio.create_task(process_transactions(wallet))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())
