# CRUD Operations Guide

This guide explains how to use the CRUD (Create, Read, Update, Delete) system in the Trading Simulator backend.

## Overview

The CRUD system provides a clean, reusable pattern for database operations. It's organized in the `app/db/crud/` directory and follows these principles:

- **Separation of Concerns**: Database operations are separated from business logic
- **Reusability**: Common operations are abstracted into a base class
- **Type Safety**: Full type hints for better IDE support and error catching
- **Consistency**: All models follow the same CRUD pattern

## Architecture

```
app/db/crud/
├── __init__.py      # Exports all CRUD classes
├── base.py          # Base CRUD class with common operations
├── user.py          # User-specific CRUD operations
└── bot.py           # Bot-specific CRUD operations
```

## Base CRUD Class

The `CRUDBase` class provides common operations for all models:

```python
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def get(self, db: Session, id: Any) -> Optional[ModelType]
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType
    def remove(self, db: Session, *, id: int) -> ModelType
```

## Creating a New CRUD Class

### 1. Create the CRUD file

```python
# app/db/crud/your_model.py
from typing import Optional
from sqlmodel import Session, select
from app.models.your_model import YourModel
from app.schemas.your_model import YourModelCreate, YourModelUpdate
from .base import CRUDBase

class CRUDYourModel(CRUDBase[YourModel, YourModelCreate, YourModelUpdate]):
    """CRUD operations for YourModel"""
    
    def get_by_custom_field(self, db: Session, *, field_value: str) -> Optional[YourModel]:
        """Get record by custom field"""
        statement = select(YourModel).where(YourModel.custom_field == field_value)
        return db.exec(statement).first()
    
    def get_by_user(self, db: Session, *, user_id: int) -> List[YourModel]:
        """Get records by user ID"""
        statement = select(YourModel).where(YourModel.user_id == user_id)
        return list(db.exec(statement).all())

# Create instance
your_model = CRUDYourModel(YourModel)
```

### 2. Update the __init__.py

```python
# app/db/crud/__init__.py
from .your_model import CRUDYourModel

__all__ = [
    "CRUDBase",
    "CRUDYourModel",
    # ... other CRUD classes
]
```

## Using CRUD in Services

```python
# app/services/your_service.py
from app.db.crud.your_model import your_model as crud_your_model
from app.schemas.your_model import YourModelCreate, YourModelInDB

class YourService:
    @staticmethod
    def create_item(db: Session, item_create: YourModelCreate) -> YourModelInDB:
        """Create a new item"""
        item = crud_your_model.create(db, obj_in=item_create)
        return YourModelInDB.model_validate(item)
    
    @staticmethod
    def get_item_by_id(db: Session, item_id: int) -> Optional[YourModelInDB]:
        """Get item by ID"""
        item = crud_your_model.get(db, item_id)
        if item:
            return YourModelInDB.model_validate(item)
        return None
```

## Using CRUD in Endpoints

```python
# app/api/api_v1/endpoints/your_endpoints.py
from app.db.crud.your_model import your_model as crud_your_model
from app.core.deps import get_current_active_user

@router.get("/", response_model=List[YourModelPublic])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> List[YourModelPublic]:
    """Get items for current user"""
    items = crud_your_model.get_by_user(db, user_id=current_user.id)
    return [YourModelPublic.model_validate(item) for item in items]

@router.post("/", response_model=YourModelPublic)
def create_item(
    item_create: YourModelCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
) -> YourModelPublic:
    """Create a new item"""
    item = crud_your_model.create_for_user(db, obj_in=item_create, user_id=current_user.id)
    return YourModelPublic.model_validate(item)
```

## Available CRUD Operations

### User CRUD (`user_crud`)

```python
# Basic operations
user_crud.get(db, user_id)                    # Get by ID
user_crud.get_multi(db, skip=0, limit=100)    # Get multiple with pagination
user_crud.create(db, obj_in=user_create)      # Create new user
user_crud.update(db, db_obj=user, obj_in=update)  # Update user
user_crud.remove(db, id=user_id)              # Delete user

# User-specific operations
user_crud.get_by_username(db, username="john")    # Get by username
user_crud.get_by_email(db, email="john@example.com")  # Get by email
user_crud.authenticate(db, username="john", password="pass")  # Authenticate
```

### Bot CRUD (`crud_bot`)

```python
# Basic operations
crud_bot.get(db, bot_id)                      # Get by ID
crud_bot.get_multi(db, skip=0, limit=100)     # Get multiple with pagination
crud_bot.create(db, obj_in=bot_data)          # Create new bot
crud_bot.update(db, db_obj=bot, obj_in=update)  # Update bot
crud_bot.remove(db, id=bot_id)                # Delete bot

# Bot-specific operations
crud_bot.get_by_user_id(db, user_id=1)        # Get bots by user
crud_bot.get_active_bots(db)                  # Get active bots
crud_bot.get_by_name(db, name="MyBot", user_id=1)  # Get by name
crud_bot.create_for_user(db, obj_in=data, user_id=1)  # Create for user
crud_bot.update_status(db, db_obj=bot, is_active=True)  # Update status
```

## Best Practices

### 1. Always Use Type Hints

```python
def get_by_custom_field(self, db: Session, *, field_value: str) -> Optional[YourModel]:
    # Implementation
```

### 2. Use Keyword-Only Arguments

```python
def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
    # Implementation
```

### 3. Handle Errors Appropriately

```python
def create_with_validation(self, db: Session, *, obj_in: CreateSchema) -> ModelType:
    # Check for duplicates
    existing = self.get_by_field(db, field=obj_in.field)
    if existing:
        raise ValueError("Field already exists")
    
    return self.create(db, obj_in=obj_in)
```

### 4. Use Proper Session Management

```python
# In endpoints
def create_item(
    item_create: ItemCreate,
    db: Session = Depends(get_db),  # Dependency injection
) -> ItemPublic:
    item = crud_item.create(db, obj_in=item_create)
    return ItemPublic.model_validate(item)
```

### 5. Convert to Schemas in Services/Endpoints

```python
# Convert database model to schema
user = user_crud.get(db, user_id)
if user:
    return UserPublic.model_validate(user)  # Convert to public schema
```

## Migration from Direct Database Queries

### Before (Direct SQLModel queries)
```python
# In service/endpoint
statement = select(User).where(User.username == username)
user = db.exec(statement).first()
```

### After (Using CRUD)
```python
# In service/endpoint
user = user_crud.get_by_username(db, username=username)
```

## Benefits

1. **Consistency**: All database operations follow the same pattern
2. **Reusability**: Common operations are abstracted and reusable
3. **Testability**: CRUD operations can be easily mocked for testing
4. **Maintainability**: Changes to database operations are centralized
5. **Type Safety**: Full type hints prevent runtime errors
6. **Documentation**: Each CRUD class documents available operations

## Testing CRUD Operations

```python
# tests/test_user_crud.py
def test_create_user(db_session):
    user_create = UserCreate(username="test", password="password")
    user = user_crud.create(db_session, obj_in=user_create)
    assert user.username == "test"
    assert user.id is not None

def test_get_by_username(db_session):
    user = user_crud.get_by_username(db_session, username="test")
    assert user is not None
    assert user.username == "test"
```

This CRUD system provides a solid foundation for all database operations in your application, making it easier to maintain and extend as your application grows.
