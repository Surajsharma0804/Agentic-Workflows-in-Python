"""Advanced plugins for elite workflows."""
from .web_scraper import WebScraperPlugin
from .image_processor import ImageProcessorPlugin
from .pdf_extractor import PDFExtractorPlugin
from .sql_query import SQLQueryPlugin
from .shell_command import ShellCommandPlugin

__all__ = [
    "WebScraperPlugin",
    "ImageProcessorPlugin", 
    "PDFExtractorPlugin",
    "SQLQueryPlugin",
    "ShellCommandPlugin"
]
