

function limpar_select(){
    list.value = '';
}

function dados_pagamento() {
    //const clienteId = document.getElementById('list').value;
    //console.log(clienteId)

   // setTimeout(function () {
     //   document.querySelector('a').style.display = 'none';
   // }, 10);
  
    //setTimeout("document.querySelector('a').style.display = 'none';", 10);


    var shownVal = document.getElementById("list").value;
    console.log(shownVal)
    //var clienteId = document.querySelector("#my-list option[value='"+shownVal+"']").dataset.value;

    teste = function(){
        return document.querySelector("#my-list option[value='"+shownVal+"']").dataset.value;
    };

    var clienteId = teste();

    console.log(clienteId)

  
    if (clienteId === "") {
        document.getElementById('financeiro-table').innerHTML = "";
        return;
    }

    fetch(`/financeiro/?id_js=${clienteId}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const financeiroList = document.getElementById('financeiro-table');
        financeiroList.innerHTML = '';
           
        const thead = document.createElement('tr');
        thead.innerHTML = `
            <thead>
                <tr>
                    <th>Código do Pagamento:</th>
                    <th>Data do Vencimento: </th>
                    <th>Data do Pagamento: </th>
                    <th>Valor da Mensalidade: </th>
                    <th>Descrição do pagamento: </th>   
                    <th>Valor com juros: </th> 
                    <th>Valor Pago:</th>
                </tr>
            </thead>
        `;
        financeiroList.appendChild(thead);

        data.financeiros.forEach(financeiro => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
            <tr>
                <td>${financeiro.id}</td>
                <td>${financeiro.data_vencimento}</td>
                <td>${financeiro.data_pagamento}</td>
                <td>${financeiro.valor_mensalidade}</td>
                <td>${financeiro.descricao_pagamento}</td>   
                <td>${financeiro.valor_com_juros}</td> 
                <td>${financeiro.valor_pago}</td>
                <td><button class = "btn btn-success" onclick="comprovante(${financeiro.id});" ">Comprovante</button></td>
                <td><button class = "btn btn-warning" onclick="editar_pagamento(${financeiro.id});" ">Editar</button></td>
                <td><button class = "btn btn-danger" onclick="excluir_pagamento(${financeiro.id});" ">Excluir</button></td>
            </tr>
            `;
            financeiroList.appendChild(tr);
        });
    })
    .catch(error => {
        console.error('Erro:', error);  
    });
}

document.addEventListener('DOMContentLoaded', (event) => {

    document.getElementById('novoPagamentoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const clienteId = document.getElementById('cliente-select-modal').value;
        const dataVencimento = document.getElementById('data-vencimento').value;
        const dataPagamento = document.getElementById('data-pagamento').value;
        const valorMensalidade = document.getElementById('valor-mensalidade').value;
        const descricaoPagamento = document.getElementById('descricao-pagamento').value;
        const valorComJuros = document.getElementById('valor-com-juros').value;
        const valorPago = document.getElementById('valor-pago').value;

        fetch('/financeiro/novo_pagamento/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                cliente_id: clienteId,
                data_vencimento: dataVencimento,
                data_pagamento: dataPagamento,
                valor_mensalidade: valorMensalidade,
                descricao_pagamento: descricaoPagamento,
                valor_com_juros: valorComJuros,
                valor_pago:valorPago


            })
        })
        .then(response => {
            if (response.ok) {
                $('#novoPagamentoModal').modal('hide');
                alert("Pagamento adicionado com sucesso!");
                dados_pagamento();  // Recarregar a lista de pagamentos após adição
            } else {
                console.error('Erro ao adicionar o pagamento.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    });
});


function comprovante(pagamentoId) {
    let result = confirm("DESEJA GERAR O COMPROVANTE PARA ESTE PAGAMENTO?");
    if (result === true) {
        fetch(`/financeiro/comprovante_generator/${pagamentoId}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('OK')
                return response.blob();
            } else {
                console.error('Erro ao gerar o comprovante.');
            }
        })
        .then(blob => {
            if (blob) {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `comprovante_${pagamentoId}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                alert("Comprovante gerado com sucesso.");
                console.log("Comprovante gerado");
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    } else {
        alert("Operação cancelada.");
        console.log("Operação cancelada");
    }
}
function excluir_pagamento(pagamentoId) {

    let result = confirm("DESEJA EXCLUIR ESTE REGISTRO?");
        if (result === true) {
            fetch(`/financeiro/delete/${pagamentoId}/`, {
                method: 'DELETE',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    dados_pagamento();  // Recarregar a lista de pagamentos após exclusão
                } else {
                    console.error('Erro ao excluir o pagamento.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
            });
            alert("Pagamento excluído com sucesso.");
            console.log("Exclusão Confirmada");
        } else {
            alert("Exclusão Cancelada.");
            console.log("Exclusão Cancelada");
        }
}

function editar_pagamento(pagamentoId) {

    let result = confirm("DESEJA EXCLUIR ESTE REGISTRO?");
        if (result === true) {
            fetch(`/financeiro/delete/${pagamentoId}/`, {
                method: 'DELETE',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    dados_pagamento();  // Recarregar a lista de pagamentos após exclusão
                } else {
                    console.error('Erro ao excluir o pagamento.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
            });
            alert("Pagamento excluído com sucesso.");
            console.log("Exclusão Confirmada");
        } else {
            alert("Exclusão Cancelada.");
            console.log("Exclusão Cancelada");
        }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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


function calcular_juros() {
    var dataPagamento = new Date(document.getElementById("data-pagamento").value);
    var dataVencimento = new Date(document.getElementById("data-vencimento").value);
    var mensalidade = Number(document.getElementById("valor-mensalidade").value);

    var diferencaDias = Math.floor((dataPagamento - dataVencimento) / (1000 * 60 * 60 * 24));
    var juros = Number(diferencaDias) * 0.33
    if (juros < 0){
        juros = 0
    }
    document.getElementById("valor-com-juros").value = mensalidade + juros;
}

function alerta_excluir() {
  alert("Tem certeza que deseja excluir?");
}

