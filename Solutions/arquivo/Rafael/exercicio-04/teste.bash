cat > solutions-rafael/exercicio-03/teste.sh <<'EOF'
#!/bin/sh
curl -i -X POST http://localhost:8000/livros \
  -H 'Content-Type: application/json' \
  -d '{"id":"101","titulo":"Fundacao","autor":"Isaac Asimov","ano":1951,"genero":"ficcao","resumo":"Teste"}'
EOF
chmod +x solutions-rafael/exercicio-03/teste.sh
git rm solutions-rafael/exercicio-04/teste.py