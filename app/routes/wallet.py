from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import WalletOperation, WalletResponse
from ..crud import get_wallet, create_wallet, update_wallet_balance
from typing import Annotated

router = APIRouter()

@router.post("/wallets", response_model=WalletResponse)
async def create_new_wallet(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await create_wallet(db)

@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
async def get_wallet_balance(
    wallet_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await get_wallet(db, wallet_id)

@router.post("/wallets/{wallet_id}/operation", response_model=WalletResponse)
async def process_wallet_operation(
    wallet_id: str,
    operation: WalletOperation,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await update_wallet_balance(
        db,
        wallet_id,
        operation.operation_type,
        operation.amount
    )
