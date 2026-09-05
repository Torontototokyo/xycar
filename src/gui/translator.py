import yaml
import os
from typing import Any, Dict, Optional

class YAMLTranslator:
    """Simple YAML-based translator with single function for language selection"""
    
    def __init__(self, locales_dir: str = './locales'):
        self.locales_dir = locales_dir
        self.translations: Dict[str, Dict] = {}
        self.current_lang: str = 'en'
        self.current_data: Dict = {}
        
        # Load all available languages
        self._load_all_languages()
        
        # Set default language
        self.set_language('en')
    
    def _load_all_languages(self):
        """Load all YAML files from locales directory"""
        if not os.path.exists(self.locales_dir):
            os.makedirs(self.locales_dir)
            return
        
        for file in os.listdir(self.locales_dir):
            if file.endswith('.yml') or file.endswith('.yaml'):
                lang_code = file.split('.')[0]
                file_path = os.path.join(self.locales_dir, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = yaml.safe_load(f)
                        
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    
    def set_language(self, lang_code: str) -> bool:
        """Single function to set/switch language"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            self.current_data = self.translations[lang_code]
            return True
        else:
            # Fallback to English if available
            if 'en' in self.translations:
                self.current_lang = 'en'
                self.current_data = self.translations['en']
            return False
    
    def get(self, key: str, **kwargs) -> str:
        """Get translation by dot notation key"""
        # Split key by dots (e.g., 'error.not_found')
        parts = key.split('.')
        value = self.current_data
        
        # Navigate through nested dictionary
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return key  # Return key if not found
        
        # If value is string, format with kwargs
        if isinstance(value, str):
            return value % kwargs if kwargs else value
        
        return str(value) if value else key
    
    def __call__(self, key: str, **kwargs) -> str:
        """Make instance callable for translation"""
        return self.get(key, **kwargs)

