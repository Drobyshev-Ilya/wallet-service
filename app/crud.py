from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from .models import Wallet
from .schemas import OperationType
from decimal import Decimal
import uuid
from fastapi import HTTPException

async def get_wallet(db: AsyncSession, wallet_id: str) -> Wallet:
    """Получает кошелёк по ID"""
    result = await db.execute(select(Wallet).where(Wallet.id == wallet_id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

async def create_wallet(db: AsyncSession) -> Wallet:
    """Создаёт новый кошелёк"""
    wallet = Wallet(id=str(uuid.uuid4()))
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

async def update_wallet_balance(
    db: AsyncSession, 
    wallet_id: str, 
    operation_type: OperationType, 
    amount: Decimal
) -> Wallet:
    """Обновляет баланс кошелька"""
    # Блокирует строку кошелька для обновления
    stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
    result = await db.execute(stmt)
    wallet = result.scalar_one_or_none()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    new_balance = wallet.balance
    if operation_type == OperationType.DEPOSIT:
        new_balance += amount
    else:  # WITHDRAW
        if wallet.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        new_balance -= amount
    
    # Обновляет с новым балансом
    wallet.balance = new_balance
    await db.commit()
    await db.refresh(wallet)
    
    return wallet
