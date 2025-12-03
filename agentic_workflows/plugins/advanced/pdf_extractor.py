"""PDF text extraction plugin."""
from typing import Dict, Any, List
from pathlib import Path
import structlog

from ..base import PluginBase

logger = structlog.get_logger()


class PDFExtractorPlugin(PluginBase):
    """
    Extract text and metadata from PDF files.
    
    Features:
    - Text extraction
    - Metadata extraction
    - Page-by-page extraction
    - Table extraction (basic)
    """
    
    name = "pdf_extractor"
    
    def __init__(self, params: Dict[str, Any], audit=None):
        super().__init__(params, audit=audit)
        self.input_path = params.get("input_path")
        self.output_path = params.get("output_path")
        self.extract_metadata = params.get("extract_metadata", True)
        self.page_range = params.get("page_range")  # e.g., "1-5" or "all"
    
    def plan(self) -> List[Dict[str, Any]]:
        return [{
            "action": "extract_pdf",
            "input": self.input_path,
            "pages": self.page_range or "all"
        }]
    
    def execute(self) -> Dict[str, Any]:
        """Extract text from PDF."""
        try:
            import PyPDF2
            
            if not Path(self.input_path).exists():
                return {"status": "error", "message": f"PDF not found: {self.input_path}"}
            
            with open(self.input_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                metadata = {}
                if self.extract_metadata:
                    info = reader.metadata
                    if info:
                        metadata = {
                            "title": info.get("/Title", ""),
                            "author": info.get("/Author", ""),
                            "subject": info.get("/Subject", ""),
                            "creator": info.get("/Creator", ""),
                            "producer": info.get("/Producer", ""),
                        }
                
                # Extract text
                num_pages = len(reader.pages)
                pages_to_extract = self._parse_page_range(self.page_range, num_pages)
                
                extracted_text = []
                for page_num in pages_to_extract:
                    if 0 <= page_num < num_pages:
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        extracted_text.append({
                            "page": page_num + 1,
                            "text": text
                        })
                
                # Combine all text
                full_text = "\n\n".join([p["text"] for p in extracted_text])
                
                # Save to file if output path specified
                if self.output_path:
                    Path(self.output_path).write_text(full_text, encoding='utf-8')
                
                if self.audit:
                    self.audit.record({
                        "plugin": self.name,
                        "input": self.input_path,
                        "pages_extracted": len(extracted_text),
                        "total_pages": num_pages
                    })
                
                return {
                    "status": "ok",
                    "metadata": metadata,
                    "num_pages": num_pages,
                    "pages_extracted": len(extracted_text),
                    "text": full_text,
                    "pages": extracted_text,
                    "output": self.output_path
                }
        
        except ImportError:
            return {"status": "error", "message": "PyPDF2 not installed"}
        except Exception as e:
            logger.error("pdf_extraction_failed", error=str(e))
            return {"status": "error", "message": str(e)}
    
    def _parse_page_range(self, page_range: str, total_pages: int) -> List[int]:
        """Parse page range string into list of page numbers."""
        if not page_range or page_range == "all":
            return list(range(total_pages))
        
        pages = []
        parts = page_range.split(",")
        
        for part in parts:
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                start = int(start) - 1  # Convert to 0-indexed
                end = int(end)
                pages.extend(range(start, end))
            else:
                pages.append(int(part) - 1)  # Convert to 0-indexed
        
        return pages
