"""Safe SQL query execution plugin."""
from typing import Dict, Any, List
import structlog

from ..base import PluginBase

logger = structlog.get_logger()


class SQLQueryPlugin(PluginBase):
    """
    Safe SQL query execution with parameterization.
    
    Features:
    - Parameterized queries (SQL injection protection)
    - Read-only mode
    - Result limiting
    - Multiple database support
    """
    
    name = "sql_query"
    
    def __init__(self, params: Dict[str, Any], audit=None):
        super().__init__(params, audit=audit)
        self.connection_string = params.get("connection_string")
        self.query = params.get("query")
        self.parameters = params.get("parameters", {})
        self.read_only = params.get("read_only", True)
        self.limit = params.get("limit", 1000)
        self.database_type = params.get("database_type", "postgresql")  # postgresql, mysql, sqlite
    
    def plan(self) -> List[Dict[str, Any]]:
        return [{
            "action": "sql_query",
            "database": self.database_type,
            "read_only": self.read_only,
            "query_preview": self.query[:100] if self.query else ""
        }]
    
    def execute(self) -> Dict[str, Any]:
        """Execute SQL query safely."""
        try:
            # Validate query if read-only mode
            if self.read_only and not self._is_read_only_query(self.query):
                return {
                    "status": "error",
                    "message": "Only SELECT queries allowed in read-only mode"
                }
            
            # Execute based on database type
            if self.database_type == "postgresql":
                return self._execute_postgresql()
            elif self.database_type == "sqlite":
                return self._execute_sqlite()
            else:
                return {"status": "error", "message": f"Unsupported database: {self.database_type}"}
        
        except Exception as e:
            logger.error("sql_query_failed", error=str(e))
            return {"status": "error", "message": str(e)}
    
    def _is_read_only_query(self, query: str) -> bool:
        """Check if query is read-only."""
        query_upper = query.strip().upper()
        write_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE"]
        return not any(keyword in query_upper for keyword in write_keywords)
    
    def _execute_postgresql(self) -> Dict[str, Any]:
        """Execute PostgreSQL query."""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                # Execute with parameters
                cursor.execute(self.query, self.parameters)
                
                if self._is_read_only_query(self.query):
                    # Fetch results with limit
                    results = cursor.fetchmany(self.limit)
                    rows = [dict(row) for row in results]
                    
                    if self.audit:
                        self.audit.record({
                            "plugin": self.name,
                            "database": "postgresql",
                            "rows_returned": len(rows)
                        })
                    
                    return {
                        "status": "ok",
                        "rows": rows,
                        "count": len(rows),
                        "limited": len(rows) == self.limit
                    }
                else:
                    conn.commit()
                    return {
                        "status": "ok",
                        "rows_affected": cursor.rowcount
                    }
            finally:
                cursor.close()
                conn.close()
        
        except ImportError:
            return {"status": "error", "message": "psycopg2 not installed"}
    
    def _execute_sqlite(self) -> Dict[str, Any]:
        """Execute SQLite query."""
        try:
            import sqlite3
            
            conn = sqlite3.connect(self.connection_string)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                cursor.execute(self.query, self.parameters)
                
                if self._is_read_only_query(self.query):
                    results = cursor.fetchmany(self.limit)
                    rows = [dict(row) for row in results]
                    
                    return {
                        "status": "ok",
                        "rows": rows,
                        "count": len(rows)
                    }
                else:
                    conn.commit()
                    return {
                        "status": "ok",
                        "rows_affected": cursor.rowcount
                    }
            finally:
                cursor.close()
                conn.close()
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
