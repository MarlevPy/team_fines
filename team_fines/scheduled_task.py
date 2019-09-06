from pathlib import Path
from datetime import datetime

wsgi_file = '/var/www/marlev89_pythonanywhere_com_wsgi.py'
Path(wsgi_file).touch()
print(f'wsgi file touched: {datetime.now()}')
