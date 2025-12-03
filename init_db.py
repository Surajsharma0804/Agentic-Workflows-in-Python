"""Initialize database tables."""
import sys
from agentic_workflows.db.database import init_db, engine
from agentic_workflows.db.models import Base

def main():
    """Create all database tables."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nTables created:")
        print("  - users (for authentication)")
        print("\nYou can now start the application!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
