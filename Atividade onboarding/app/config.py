"""Configuracoes lidas das variaveis de ambiente."""

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://tot:tot@localhost:5432/vddb",
)
