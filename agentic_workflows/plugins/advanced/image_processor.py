"""Image processing plugin with OCR support."""
from typing import Dict, Any, List
from pathlib import Path
import structlog

from ..base import PluginBase

logger = structlog.get_logger()


class ImageProcessorPlugin(PluginBase):
    """
    Image processing with Pillow and OCR.
    
    Features:
    - Resize, crop, rotate
    - Format conversion
    - OCR text extraction
    - Thumbnail generation
    - Metadata extraction
    """
    
    name = "image_processor"
    
    def __init__(self, params: Dict[str, Any], audit=None):
        super().__init__(params, audit=audit)
        self.input_path = params.get("input_path")
        self.output_path = params.get("output_path")
        self.operation = params.get("operation", "info")  # info, resize, ocr, thumbnail
        self.width = params.get("width")
        self.height = params.get("height")
        self.format = params.get("format")  # jpg, png, webp
        self.quality = params.get("quality", 85)
    
    def plan(self) -> List[Dict[str, Any]]:
        return [{
            "action": f"image_{self.operation}",
            "input": self.input_path,
            "output": self.output_path
        }]
    
    def execute(self) -> Dict[str, Any]:
        """Execute image processing."""
        try:
            from PIL import Image
            
            if not Path(self.input_path).exists():
                return {"status": "error", "message": f"Image not found: {self.input_path}"}
            
            img = Image.open(self.input_path)
            
            if self.operation == "info":
                return self._get_info(img)
            elif self.operation == "resize":
                return self._resize(img)
            elif self.operation == "thumbnail":
                return self._thumbnail(img)
            elif self.operation == "ocr":
                return self._ocr(img)
            elif self.operation == "convert":
                return self._convert(img)
            else:
                return {"status": "error", "message": f"Unknown operation: {self.operation}"}
        
        except ImportError:
            return {"status": "error", "message": "Pillow not installed"}
        except Exception as e:
            logger.error("image_processing_failed", error=str(e))
            return {"status": "error", "message": str(e)}
    
    def _get_info(self, img) -> Dict[str, Any]:
        """Get image information."""
        return {
            "status": "ok",
            "info": {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height
            }
        }
    
    def _resize(self, img) -> Dict[str, Any]:
        """Resize image."""
        if not self.width or not self.height:
            return {"status": "error", "message": "Width and height required for resize"}
        
        resized = img.resize((self.width, self.height))
        resized.save(self.output_path, quality=self.quality)
        
        if self.audit:
            self.audit.record({
                "plugin": self.name,
                "operation": "resize",
                "from_size": img.size,
                "to_size": (self.width, self.height)
            })
        
        return {
            "status": "ok",
            "operation": "resize",
            "output": self.output_path,
            "original_size": img.size,
            "new_size": (self.width, self.height)
        }
    
    def _thumbnail(self, img) -> Dict[str, Any]:
        """Create thumbnail."""
        size = (self.width or 128, self.height or 128)
        img.thumbnail(size)
        img.save(self.output_path, quality=self.quality)
        
        return {
            "status": "ok",
            "operation": "thumbnail",
            "output": self.output_path,
            "size": img.size
        }
    
    def _ocr(self, img) -> Dict[str, Any]:
        """Extract text using OCR."""
        try:
            import pytesseract
            text = pytesseract.image_to_string(img)
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "operation": "ocr",
                    "text_length": len(text)
                })
            
            return {
                "status": "ok",
                "operation": "ocr",
                "text": text,
                "length": len(text)
            }
        except ImportError:
            return {
                "status": "error",
                "message": "pytesseract not installed"
            }
    
    def _convert(self, img) -> Dict[str, Any]:
        """Convert image format."""
        if not self.format:
            return {"status": "error", "message": "Format required for conversion"}
        
        img.save(self.output_path, format=self.format.upper(), quality=self.quality)
        
        return {
            "status": "ok",
            "operation": "convert",
            "output": self.output_path,
            "from_format": img.format,
            "to_format": self.format
        }
