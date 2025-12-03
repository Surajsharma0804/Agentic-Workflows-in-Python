"""PostgreSQL operations plugin."""
from ..base import PluginBase
import psycopg2
from typing import List, Dict, Any

class PostgreSQLPlugin(PluginBase):
    """PostgreSQL database operations."""
    
    name = "postgresql"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.connection_string = params.get("connection_string")
        self.query = params.get("query")
        self.operation = params.get("operation", "select")  # select, insert, update, delete
    
    def plan(self) -> list:
        return [{"action": f"postgres_{self.operation}", "query": self.query[:100]}]
    
    def execute(self) -> dict:
        try:
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor()
            
            cursor.execute(self.query)
            
            if self.operation == "select":
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
            else:
                conn.commit()
                data = {"rows_affected": cursor.rowcount}
            
            cursor.close()
            conn.close()
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "operation": self.operation,
                    "rows": len(data) if isinstance(data, list) else data.get("rows_affected", 0)
                })
            
            return {"status": "ok", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}
