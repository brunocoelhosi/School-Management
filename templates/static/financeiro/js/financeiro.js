function limpar_select(){
    list.value = '';
}

function dados_pagamento() {
   
    var nomeCliente = document.getElementById("list").value;
    console.log(nomeCliente)
    //var clienteId = document.querySelector("#my-list option[value='"+shownVal+"']").dataset.value;

    teste = function(){
        return document.querySelector("#my-list option[value='"+nomeCliente+"']").dataset.value;
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
                
                <td><button class="btn btn-success" onclick="comprovante(${financeiro.id}, '${nomeCliente}');">Comprovante</button></td>
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
                Swal.fire({
                    title: "Sucesso!",
                    text: "Pagamento adicionado com sucesso!",
                    icon: "success"
                  });
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


function comprovante(pagamentoId,shownVal) {
    
    Swal.fire({
        title: "Deseja gerar o comprovante para esse pagamento?",
        text: "",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelButtonText: "Cancelar!",
        confirmButtonText: "Sim!"
        }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/financeiro/comprovante_generator/${pagamentoId}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {

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
                a.download = `comprovante_${pagamentoId}_${shownVal}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                Swal.fire({
                    title: "Sucesso!",
                    text: "Comprovante gerado com sucesso.",
                    icon: "success"
                
                    });
                
                console.log("Comprovante gerado");
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    } else {
       // alert("Operação cancelada.");
        console.log("Operação cancelada");
    }
    }
    );  
}


function editar_pagamento(pagamentoId) {

    Swal.fire({
        title: "Você tem certeza?",
        text: "Deseja editar este comprovante?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim!"
      }).then((result) => {
        if (result.isConfirmed) {
            fetch(``, {
                method: 'DELETE',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    Swal.fire({
                        title: "Sucesso!",
                        text: "Comprovante excluído com sucesso.",
                        icon: "success"
                      });
                    dados_pagamento(); //reload lista de pagamentos
                } else {
                    console.error('Erro ao excluir o comprovante.');
                    alert("Erro ao excluir o comprovante.");
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert("Erro ao excluir o comprovante.");
            });
    
            console.log("Exclusão Confirmada");
        } else {
            console.log("Exclusão Cancelada");
        }
        }
      );
}

function excluir_pagamento(pagamentoId) {

    Swal.fire({
        title: "Você tem certeza?",
        text: "Você não será capaz de reverter isso!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sim, exclua esse comprovante!"
      }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/financeiro/delete/${pagamentoId}/`, {
                method: 'DELETE',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    Swal.fire({
                        title: "Sucesso!",
                        text: "Comprovante excluído com sucesso.",
                        icon: "success"
                      });
                    dados_pagamento(); //reload lista de pagamentos
                } else {
                    console.error('Erro ao excluir o comprovante.');
                    alert("Erro ao excluir o comprovante.");    
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert("Erro ao excluir o comprovante");
            });
    
            console.log("Exclusão Confirmada");
        } else {
            console.log("Exclusão Cancelada");
        }
        }
      );


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

