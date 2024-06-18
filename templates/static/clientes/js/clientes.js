document.addEventListener('DOMContentLoaded', (event) => {
    dados_cliente();
    calcular();
    limpar_select()
});

function exibir_form(tipo){

    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if(tipo == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    }else if(tipo == "2"){
        add_cliente.style.display = "none";
        att_cliente.style.display = "block"
    }

}


function dados_cliente(){

    // pegar id cliente na list/select
    var shownVal = document.getElementById("cliente_select").value;
    var id_cliente = document.querySelector("#my-list option[value='"+shownVal+"']").dataset.value;

    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
        

    },console.log(csrf_token)).then(function(result){
        return result.json()
    }).then(function(data){
        document.getElementById('form-att-cliente').style.display = 'block'
        
        id = document.getElementById('id')
        id.value = data['cliente_id']

        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        datanascimento = document.getElementById('datanascimento')
        datanascimento.value = data['cliente']['datanascimento']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        endereco = document.getElementById('endereco')
        endereco.value = data['cliente']['endereco']

        bairro = document.getElementById('bairro')
        bairro.value = data['cliente']['bairro']

        cep = document.getElementById('cep')
        cep.value = data['cliente']['cep']

        cidade = document.getElementById('cidade')
        cidade.value = data['cliente']['cidade']

        estado = document.getElementById('estado2')
        estado.value = data['cliente']['estado']

        telefone = document.getElementById('telefone')
        telefone.value = data['cliente']['telefone']

        celular = document.getElementById('celular')
        celular.value = data['cliente']['celular']

        nome_responsavel = document.getElementById('nome_responsavel')
        nome_responsavel.value = data['cliente']['nome_responsavel']

        cpf_responsavel = document.getElementById('cpf_responsavel')
        cpf_responsavel.value = data['cliente']['cpf_responsavel']

        nascimento_responsavel = document.getElementById('nascimento_responsavel')
        nascimento_responsavel.value = data['cliente']['nascimento_responsavel']

        telefone_responsavel = document.getElementById('telefone_responsavel')
        telefone_responsavel.value = data['cliente']['telefone_responsavel']

        cursos = document.getElementById('cursos')
        cursos.value = data['cliente']['cursos']

        duracao = document.getElementById('duracao')
        duracao.value = data['cliente']['duracao']

        inicio = document.getElementById('inicio')
        inicio.value = data['cliente']['inicio']

        dias_curso = document.getElementById('dias_curso')
        dias_curso.value = data['cliente']['dias_curso']

        horarios_curso = document.getElementById('horarios_curso')
        horarios_curso.value = data['cliente']['horarios_curso']

        instrutor = document.getElementById('instrutor')
        instrutor.value = data['cliente']['instrutor']

        mensalidade = document.getElementById('mensalidade')
        mensalidade.value = data['cliente']['mensalidade']

        parcelas = document.getElementById('parcelas')
        parcelas.value = data['cliente']['parcelas']

        dia_pagamento = document.getElementById('dia_pagamento')
        dia_pagamento.value = data['cliente']['dia_pagamento']

        total = document.getElementById('total_calculo2')
        total.value = data['cliente']['total']            
     
    })
    

}



function update_cliente(){

    nome = document.getElementById('nome').value
    cpf = document.getElementById('cpf').value
    datanascimento = document.getElementById('datanascimento').value
    email = document.getElementById('email').value    
    endereco = document.getElementById('endereco').value
    bairro = document.getElementById('bairro').value
    cep = document.getElementById('cep').value
    cidade = document.getElementById('cidade').value
    estado = document.getElementById('estado2').value
    telefone = document.getElementById('telefone').value
    celular = document.getElementById('celular').value
    nome_responsavel = document.getElementById('nome_responsavel').value
    cpf_responsavel = document.getElementById('cpf_responsavel').value
    nascimento_responsavel = document.getElementById('nascimento_responsavel').value
    telefone_responsavel = document.getElementById('telefone_responsavel').value
    cursos = document.getElementById('cursos').value
    duracao = document.getElementById('duracao').value
    inicio = document.getElementById('inicio').value
    dias_curso = document.getElementById('dias_curso').value
    horarios_curso = document.getElementById('horarios_curso').value
    instrutor = document.getElementById('instrutor').value
    mensalidade = document.getElementById('mensalidade').value
    parcelas = document.getElementById('parcelas').value
    dia_pagamento = document.getElementById('dia_pagamento').value
    total = document.getElementById('total_calculo2').value
    id = document.getElementById('id').value

    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            cpf: cpf,
            datanascimento: datanascimento,
            email: email,
            endereco: endereco,
            bairro: bairro,
            cep: cep,
            cidade: cidade,
            estado: estado,
            telefone: telefone, 
            celular: celular,
            nome_responsavel: nome_responsavel,
            cpf_responsavel: cpf_responsavel,
            nascimento_responsavel: nascimento_responsavel,
            telefone_responsavel: telefone_responsavel, 
            cursos: cursos, 
            duracao: duracao,
            inicio: inicio, 
            dias_curso: dias_curso, 
            horarios_curso: horarios_curso, 
            instrutor: instrutor, 
            parcelas: parcelas,
            dia_pagamento: dia_pagamento,
            mensalidade: mensalidade, 
            total: total,
        })

    }).then(function(result){
        return result.json()
    }).then(function(data){

        if(data['status'] == '200'){
            nome = data['nome']
            cpf = data['cpf']
            datanascimento = data['datanascimento']
            email = data['email']
            endereco = data['endereco']
            bairro = data['bairro']
            cep = data['cep']
            cidade = data['cidade']
            estado = data['estado']
            telefone = data['telefone']
            celular = data['celular']
            nome_responsavel = data['nome_responsavel']
            cpf_responsavel = data['cpf_responsavel']
            nascimento_responsavel = data['nascimento_responsavel']
            telefone_responsavel = data['telefone_responsavel']
            cursos = data['cursos']
            duracao = data['duracao']
            inicio = data['inicio']
            dias_curso = data['dias_curso']
            horarios_curso = data['horarios_curso']
            instrutor = data['instrutor']
            mensalidade = data['mensalidade']
            parcelas = data['parcelas']
            dia_pagamento = data['dia_pagamento']
            total = data['total']
         
            //console.log('Dados alterados com sucesso')
            //var resultado = document.getElementById("resultado_cadastro")
            //resultado.innerHTML = '<div id="resultado_cadastro" class= "alert alert-success" role="alert" style="text-align:center">Cadastro realizado com sucesso!</div>'
            alert("Dados atualizados com sucesso!");
        }else{
            alert('Ocorreu algum erro');
        }

    })

}

function calcular() {
    var num1 = Number(document.getElementById("num1").value);
    var num2 = Number(document.getElementById("num2").value);
    //var elemResult = document.getElementById("resultado");
    document.getElementById("total_calculo").value = parseFloat(num1 * num2).toFixed(2);

 
}

function excluir_cliente(id) {

    id = +document.getElementById("cliente-select").value
    console.log(typeof(id))
    if (typeof id !== 'number') {
        console.error('ID inválido: ', id);
        alert('ID do cliente é inválido.');
        return;
    }

    let result = confirm("DESEJA EXCLUIR ESTE CLIENTE?");
    if (result === true) {
        fetch(`/clientes/excluir_cliente/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                alert("Cliente excluído com sucesso.");
                //location.reload(); // Recarregar a pagina apos exlcusao
                //redirect
                window.history.pushState({}, document.title, "/clientes/");
                location.reload();
            } else {
                console.error('Erro ao excluir o cliente.');
                alert("Erro ao excluir o cliente.");
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert("Erro ao excluir o cliente.");
        });

        console.log("Exclusão Confirmada");
    } else {
        console.log("Exclusão Cancelada");
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Verifica se este cookie começa com o nome que queremos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function alerta(){

    alert("teste")
}

function limpar_select(){
    cliente_select.value = '';
}