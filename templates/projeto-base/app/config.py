"""Configurações lidas das variáveis de ambiente (definidas no compose.yaml)."""

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://tot:tot@localhost:5432/vddb")
