import json
import re
import uuid
import datetime
from pathlib import Path
from typing import Dict, Any, List

class LayoutService:
    def __init__(self, base_dir: Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd() / 'layouts'
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _slugify(self, name: str) -> str:
        slug = re.sub(r'[^a-zA-Z0-9_-]+', '_', name).strip('_').lower()
        return slug or uuid.uuid4().hex

    def _layout_path(self, name: str) -> Path:
        return self.base_dir / f'{self._slugify(name)}.json'

    def create_layout(self, layout: Dict[str, Any]) -> str:
        layout_id = self._slugify(layout['name'])
        layout['created_at'] = datetime.datetime.utcnow().isoformat()
        with open(self._layout_path(layout['name']), 'w', encoding='utf-8') as f:
            json.dump(layout, f, ensure_ascii=False, indent=2)
        return layout_id

    def list_layouts(self) -> List[Dict[str, Any]]:
        layouts: List[Dict[str, Any]] = []
        for p in self.base_dir.glob('*.json'):
            try:
                with open(p, encoding='utf-8') as f:
                    layouts.append(json.load(f))
            except Exception:
                continue
        return layouts

    def layout_exists(self, name: str) -> bool:
        return self._layout_path(name).exists()

    def load_layout(self, name: str) -> Dict[str, Any]:
        with open(self._layout_path(name), encoding='utf-8') as f:
            return json.load(f)
