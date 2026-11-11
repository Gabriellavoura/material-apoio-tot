#!/bin/sh
set -eu

aws s3 mb s3://rafael-bucket-1
aws s3 mb s3://rafael-bucket-2

echo "Teste de upload Rafael" > teste.txt
aws s3 cp teste.txt s3://rafael-bucket-1/