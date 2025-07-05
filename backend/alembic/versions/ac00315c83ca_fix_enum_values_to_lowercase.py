"""Fix enum values to lowercase

Revision ID: ac00315c83ca
Revises: c0b0c7db76ef
Create Date: 2025-07-05 12:12:50.941133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac00315c83ca'
down_revision: Union[str, Sequence[str], None] = 'c0b0c7db76ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
     # For PostgreSQL, you need to recreate the enum
    op.execute("ALTER TYPE transactiontype RENAME TO transactiontype_old")
    
    # Create new enum with lowercase values
    op.execute("CREATE TYPE transactiontype AS ENUM ('income', 'expense')")
    
    # Update the column to use the new enum
    op.execute("""
        ALTER TABLE transactions 
        ALTER COLUMN type TYPE transactiontype 
        USING type::text::transactiontype
    """)
    
    # Drop the old enum
    op.execute("DROP TYPE transactiontype_old")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE transactiontype RENAME TO transactiontype_old")
    op.execute("CREATE TYPE transactiontype AS ENUM ('INCOME', 'EXPENSE')")
    op.execute("""
        ALTER TABLE transactions 
        ALTER COLUMN type TYPE transactiontype 
        USING type::text::transactiontype
    """)
    op.execute("DROP TYPE transactiontype_old")
