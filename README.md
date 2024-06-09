<h2>Sistema de Gerenciamento de Escolas</h2>

Sistema completo de gestão escolar, academico e financeiro.
<br>
<br>
<h3>Tecnologias: </h3>
Python, Django, PostgreSql, Html, Css, Bootstrap.</h3>

<br>
<h3>Foram utilizadas as seguintes rotas:</h3>
<h4>Rotas Cliente:</h3>

POST `clientes/atualiza_cliente/` - utilizada para cadastrar um cliente

`update_cliente/<int:id>` - utilizada para atualizar os dados de um cliente

`excluir_cliente/<int:id>` - utilizada para excluir o cadastro de um cliente

<br>  
<br>
<h4>Rotas Sistema Financeiro:</h3>

DELETE `financeiro/delete/<int:pagamento_id>/` - utilizada para excluir um pagamento realizado

POST `financeiro/novo_pagamento/` - utilizada para cadastrar um novo pagamento 
<br>




