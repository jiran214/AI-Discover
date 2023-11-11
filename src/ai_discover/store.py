import dataset
from dataset import Database, Table

import cfg

db_name = 'ai_discover.db'

db: Database = dataset.connect(f'sqlite:///{cfg.db_dir/db_name}')
bilibili_note_store: Table = db['bilibili_note']