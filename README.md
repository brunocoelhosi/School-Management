## Sistema de Gerenciamento de Escolas

Sistema completo de gestão escolar, academico e financeiro.
<br><br>
## Tecnologias utilizadas:
Python, Django, PostgreSql, Html, Css, Bootstrap.</h3>
<br><br>
## Funcionalidades

#### Cliente:

`Cadastro, exclusão e update dos dados dos alunos.`

#### Financeiro:

`Cadastro, exclusão e update dos dados de pagamento realizado pelos alunos.`

`Geração recibos em PDF dos pagamentos recebidos.`

#### Mapa de Horário (Em desenvolvimento):

`Criação de um mapa de horário para visualização dos horários disponíveis na sala de aula.`

#### Faturamento (Em desenvolvimento):

`Apresentação do faturamento diário, mensal e anual através de gráficos.`
<br><br>

## Demonstração
#### Front End: <a href="https://siscursos.com.br/" target="_blank">Clique Aqui</a>
<br>
<img src="https://github.com/brunocoelhosi/School-Management/blob/master/Screenshot_3.png" style="width:640px;height:auto;"></a>

#### Back End (Painel de cadastro)
<br><img src="https://github.com/brunocoelhosi/School-Management/blob/master/Screenshot_1.png" style="width:640px;height:auto;"></a>
<br><img src="https://github.com/brunocoelhosi/School-Management/blob/master/Screenshot_2.png" style="width:640px;height:auto;"></a>
<br><br>
## Pré-requisitos

Antes de executar o script, certifique-se de ter os seguintes requisitos instalados:

- Python 3.x
- Bibliotecas Python (listadas no `requirements.txt`)
<br><br>
## Como Usar

Siga os passos abaixo para configurar e executar o projeto:

1. Clone este repositório:
   ```bash
   git clone https://github.com/brunocoelhosi/School-Management.git
2. Crie um ambiente virtual no diretório do projeto
3. Instale as dependências
   ```bash
   pip install -r requirements.txt
4. Aplicar as migrações
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
5. Executar o servidor
   ```bash
   python manage.py runserver
