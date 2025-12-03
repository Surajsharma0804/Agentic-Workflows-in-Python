"""
Vercel entrypoint for FastAPI application.
This file is required by Vercel to detect and deploy the FastAPI app.
"""
from agentic_workflows.api.server import app

# Export the app for Vercel
__all__ = ['app']
