# op7-vtracer

Landing page OP7 exportada da VPS cypher em 07/10/2026.

- **Domínio:** tracer.op7franquia.com.br
- **Como roda:** Python 3.11 + binário vtracer (Dockerfile), porta 5000
- **Subir:** `docker build -t op7-vtracer .` e `docker run -d -p <porta>:<porta da linha acima> op7-vtracer`
- **Atenção:** Ferramenta interna (imagem -> SVG), sem login.
