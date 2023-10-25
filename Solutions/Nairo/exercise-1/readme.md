**Descrição**

API flask, com duas rotas não bloqueantes e paralelas, de forma que suporte processamentos longos (horas de duração):

*  Rota `/` raiz da aplicação

*  Rota `/health` para checar o healthcheck do container, mostrar filas e buckets existentes e o conteúdo de cada bucket.