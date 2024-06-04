<h2>Sistema de Gerenciamento de Escolas</h2>

Sistema completo de gestão escolar, academico e financeiro.
<br>
<br>
<h3>Technologies: Python, Django, PostgreSql, Html, Css, Bootstrap.</h3>

Este projeto é uma API REST para atender a aplicação de uma carteira digital.

Foram utilizadas as seguintes rotas:
<br>
<br>
<h3>Rotas Cliente:</h3>

`clientes/atualiza_cliente/` - utilizada para atualizar os dados de um cliente

`update_cliente/<int:id>` - utilizada para atualizar os dados de um cliente

`excluir_cliente/<int:id>` - utilizada para excluir o cadastro de um cliente

<br>
<br>
<h3>Rotas sistema Financeiro:</h3>

DELETE `financeiro/delete/<int:pagamento_id>/` - utilizada para excluir um pagamento realizado

POST `financeiro/novo_pagamento/` - utilizada para cadastrar um novo pagamento 
<br>




