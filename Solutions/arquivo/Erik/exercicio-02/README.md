# Para Pensar

### Envie duas mensagens com o mesmo `--message-deduplication-id`. Quantas chegam na fila? Por quê?
**Resposta:** Chega apenas uma na fila, pois o MessageDeduplicationId é um identificador único da mensagem que serve para evitar duplicatas. Nesse caso, impedindo que duas mensagens iguais sejam enviadas.

---

### O que acontece se você ler uma mensagem e não apagá-la? Espere 30 segundos e leia de novo. Pesquise o que é visibility timeout na documentação do SQS.
**Resposta:** Quando lemos uma mensagem ela entra em visibility timeout no qual a mensagem fica invisível para todo o resto para que possamos trabalhar nela. Se até o fim do tempo estipulado nenhuma ação for feita, ela volta a ficar visível.