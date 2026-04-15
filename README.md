# FlaskBiblioteca - projeto de Biblioteca Online

**FlaskBiblioteca** é um projeto de _biblioteca online_ baseado no meu TCC, usando o framework Flask e suas extensões. O Objetivo do projeto é fornecer uma plataforma de fácil uso para o gerenciamento de livros e emmpréstimos.

## Funcionalidades

Cadastro de livros, Cadastro de usuários, Empréstimos e devolução, busca por livros, autenticação, e autorização, painel adminsitrativo.

### Linguagens

* Python
* HTML
* CSS
* JavaScript
* SQL

### Funcionalidades a serem desenvolvidas

1. Sistema de notificações por e-mail
2. Integração com APIs de terceiros para busca de livros
3. Melhorias na interface do usuário
4. Implementação de testes automatizados
5. Suporte a múltiplos idiomas

### imagem

![icone de erro 404](app/src/frontend/static/images/error/page_not_found.png)

### links dos pacotes

[extensions](app/src/backend/extensions)

[icones![icons](app/src/frontend/static/images/icons/calendar.png)](app/src/frontend/static/images/icons/)

### exemplo do init

```Python

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    return app
```

### TASK LIST

* [x] Configuração do ambiente Flask
* [x] Criação do modelo de dados
* [x] Implementação das rotas principais
* [ ] Testes unitários
* [ ] Documentação da API

testando alternativa dos markdown
=================================

subtitulo agora
---------------

## closed atx ##

* item 1
  * item 2
    * item 3

Some text

        * hard tab character used to indent the list item

Some text

    * Spaces used to indent the list item insteadem instead

$ ls
README.md

$ cd
$ mkdir

$ ls
$ cat foo
$ less bar