from pydantic import BaseSettings

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

graylog_settings = {}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'encoding': 'utf-8',
    'formatters': {
        'simple': {
            'format': "[%(asctime)s]-[%(levelname)s|%(filename)s:%(lineno)s]-[%(message)s]",
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'logfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'when': 'D',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'backupCount': 20,
        },
        **graylog_settings
    },
    'loggers': {
        'fastapi': {
            'handlers': ['console', 'logfile'] + (['pygelf'] if graylog_settings else []),
            'level': 'DEBUG',
        }
    },
}


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    KUBEFLOW_ENDPOINT: str
    KUBEFLOW_USERNAME: str
    KUBEFLOW_PASSWORD: str

    S3_ENDPOINT: str
    KUBERFLOW_NAMESPACE: str
    MINIO_USERNAME: str
    MINIO_KEY: str
    MINIO_REGION: str

    SAMPLE_COMP_DIR: str
    SAMPLE_COMP_BUCKET: str

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"


settings = Settings()
