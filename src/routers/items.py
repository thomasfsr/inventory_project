from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.tables import User, InventoryItem
from src.schemas import (
    FilterItem,
    Message,
    ItemList,
    ItemPublic,
    ItemSchema,
    ItemUpdate,
)
from src.security import get_current_user

router = APIRouter()

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/items', tags=['items'])


@router.post('/', response_model=ItemPublic)
def create_item(
    item: ItemSchema,
    user: CurrentUser,
    session: T_Session,
):
    db_item: InventoryItem = InventoryItem(
        user_id=user.id,
        name=item.name,
        description=item.description,
        location= item.location,
        quantity=item.quantity,
        unit= item.item,
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.get('/', response_model=ItemList)
def list_items(
    session: T_Session,
    user: CurrentUser,
    item_filter: Annotated[FilterItem, Query()],
):
    query = select(InventoryItem).where(InventoryItem.user_id == user.id)

    if item_filter.title:
        query = query.filter(InventoryItem.name.contains(item_filter.name))

    if item_filter.description:
        query = query.filter(
            InventoryItem.description.contains(item_filter.description)
        )

    if item_filter.state:
        query = query.filter(InventoryItem.state == item_filter.state)

    items = session.scalars(
        query.offset(item_filter.offset).limit(item_filter.limit)
    ).all()

    return {'items': items}


@router.patch('/{item_id}', response_model=ItemPublic)
def patch_item(
    item_id: int, session: T_Session, user: CurrentUser, item: ItemUpdate
):
    db_item = session.scalar(
        select(InventoryItem).where(InventoryItem.user_id == user.id, 
                                    InventoryItem.id == item_id)
    )

    if not db_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Item not found.'
        )

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item


@router.delete('/{item_id}', response_model=Message)
def delete_item(item_id: int, session: T_Session, user: CurrentUser):
    item = session.scalar(
        select(InventoryItem).where(InventoryItem.user_id == user.id, 
                                    InventoryItem.id == item_id)
    )

    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Item not found.'
        )

    session.delete(item)
    session.commit()

    return {'message': 'Item has been deleted successfully.'}