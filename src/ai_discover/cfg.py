from pathlib import Path

work_dir = Path('/').parent.absolute()
db_dir = work_dir / 'db'
chunk_size = 250