# UD16 — Esiti del laboratorio guidato

## Configurazione e avvio

Indica ConfigMap, Secret dimostrativo, file montato e immagini utilizzate.

```bash
$ kubectl --context=minikube -n ft152-catalogo get configmap catalog-config
NAME             DATA   AGE
catalog-config   4      6s
$ kubectl --context=minikube -n ft152-catalogo get secret catalog-demo
NAME           TYPE     DATA   AGE
catalog-demo   Opaque   1      5s
```

Immagini utilizzate: `localhost/catalog-backend:ud16` | `localhost/catalog-frontend:ud16`

## Persistenza prima/dopo

Registra nome del Pod e valore del contatore **prima e dopo** la ricreazione, con interpretazione.

- Nome Prima Creazione: `backend-59b9668f45-drw2g`
- Valore Contatore: `1`
- Nome Dopo Creazione: `backend-59b9668f45-c4qsz`
- Valore Contatore: `2`

## Service, DNS e proxy

Descrivi nome risolto, EndpointSlice e risposta HTTP.

## Gateway e HTTPRoute

Riporta condizioni e risultato della richiesta con `Host: catalogo.lab`, o il prerequisito che ha impedito la verifica.

## Collegamento architetturale e accesso

- Oggetto configurato e componente che realizza il comportamento:
- Prova reale, momento e interpretazione:
- Indirizzo e percorso verificato (specificare se Gateway o diagnostica diretta):
- Stato dell’ingresso locale e limiti della prova:
