import os
from pathlib import Path
import hashlib
from typing import Optional
import logging
from datetime import datetime
import json

class NFTUtils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def generate_unique_id(content: str) -> str:
        """Generate a unique ID based on content"""
        return hashlib.sha256(content.encode()).hexdigest()[:12]
    
    @staticmethod
    def create_output_directory(base_dir: str = "output") -> Optional[Path]:
        """Create timestamped output directory"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path(base_dir) / timestamp
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir
        except Exception as e:
            logging.error(f"Error creating output directory: {str(e)}")
            return None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to be safe for all operating systems"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def save_generation_info(self, output_dir: Path, prompt: str, params: dict) -> bool:
        """Save generation parameters to a file"""
        try:
            info_file = output_dir / "generation_info.json"
            generation_info = {
                "prompt": prompt,
                "parameters": params,
                "timestamp": datetime.now().isoformat(),
            }
            
            with info_file.open('w') as f:
                json.dump(generation_info, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Error saving generation info: {str(e)}")
            return False
    
    @staticmethod
    def get_file_hash(file_path: Path) -> Optional[str]:
        """Calculate SHA-256 hash of a file"""
        try:
            sha256_hash = hashlib.sha256()
            with file_path.open("rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logging.error(f"Error calculating file hash: {str(e)}")
            return None

class PromptHelper:
    @staticmethod
    def enhance_prompt(prompt: str, style: Optional[str] = None) -> str:
        """Enhance prompt with additional style information"""
        style_templates = {
            "realistic": "ultra realistic, highly detailed, 8k resolution, professional photography",
            "anime": "anime style, cel shaded, vibrant colors, detailed illustration",
            "abstract": "abstract art style, creative, artistic, modern art interpretation",
            "digital": "digital art, clean lines, modern design, professional illustration"
        }
        
        if style and style in style_templates:
            return f"{prompt}, {style_templates[style]}"
        return prompt
    
    @staticmethod
    def generate_negative_prompt() -> str:
        """Generate a standard negative prompt for better quality"""
        return "blurry, low quality, distorted, deformed, ugly, bad anatomy, watermark, signature, text" 