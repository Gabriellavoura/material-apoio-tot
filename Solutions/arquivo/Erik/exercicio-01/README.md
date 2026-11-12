# Exercício 01 - Buckets S3

## Recursos confirmados

O script de inicialização cria:

- `bucket-1`
- `bucket-2`

## Comandos usados para conferir

```shell
aws --profile floci s3 mb s3://bucket-1
aws --profile floci s3 mb s3://bucket-2
aws --profile floci s3 ls
aws --profile floci s3 cp teste.txt s3://bucket-1/
aws --profile floci s3 cp s3://bucket-1/teste.txt s3://bucket-2/
```

## Resultado esperado

```text
make_bucket: bucket-1
make_bucket: bucket-2
2026-11-10 17:19:00       10 teste.txt
copy: s3://bucket-1/teste.txt to s3://bucket-2/teste.txt
```