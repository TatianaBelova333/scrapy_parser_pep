from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

STRING_LENGTH = 200
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
RESULTS_FOLDER = 'results'
RESULTS_DIR = BASE_DIR / RESULTS_FOLDER

STATUS_SUMMARY_COLS = ('Статус', 'Количество')

PEP_NUM_GRP = 'pep_number'
PEP_NAME_GRP = 'pep_name'
PEP_NUM_NAME_SRCH_PATN = (fr'PEP (?P<{PEP_NUM_GRP}>\d{{1,4}}) – '
                          fr'(?P<{PEP_NAME_GRP}>.*)')

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'pep_parser.logs'
LOG_DATEFORMAT = DATETIME_FORMAT
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
LOG_LEVEL = 'DEBUG'
LOG_FILE_APPEND = True

FEEDS = {
    f'{RESULTS_FOLDER}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True,
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

ROBOTSTXT_OBEY = True
