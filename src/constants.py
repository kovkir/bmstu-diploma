# размеры окна приложения
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600

# для выбора метода кластеризации
HA           = 0
K_PROTOTYPES = 1
HYBRID       = 2

# для выбора метода сравнения
EVALUATION_SILHOUETTES = 0
ELBOW                  = 1

# для инициализации
NUMBER_OF_CLUSTERS = 30
NUMBER_OF_OBJECTS  = 80
NUMBER_OF_RUNS     = 10

# используемые файлы
FILE_NAME = "../docs/data/best_result.csv"
# FILE_NAME = "../docs/data/fifa_players.csv"
# FILE_NAME = "../docs/data/fifa_players2.csv"
BACKUP_FILE_NAME = "../docs/data/backup.csv"

# информация о данных в файле
NUMERIC_COLUMNS = [1, 4]
RANGES_LIST     = [23, 214500]
NUMBER_OF_ROWS  = 3000
