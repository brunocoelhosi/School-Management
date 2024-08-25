function limpar_select(){
    list.value = '';
}

function dados_pagamento() {

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


}

function contrato() {

    var nomeCliente = document.getElementById("list").value; //get nome
    console.log(nomeCliente)
    var clienteId = document.querySelector("#my-list option[value='"+nomeCliente+"']").dataset.value; //id
    console.log(clienteId)

    Swal.fire({
        title: "Deseja gerar o contrato deste aluno?",
        text: "",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelButtonText: "Cancelar!",
        confirmButtonText: "Sim!"
        }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/historico/contrato_generator/${clienteId}/`, {
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
                    
                    Swal.fire({
                        title: "Erro ao gerar o contrato.",
                        text: "Confira os campos: (Data do Pagamento, Data de Vencimento, Data de Nascimento e Data de Inicio)",
                        icon: "warning"
                    });

                    console.error('Erro ao gerar o contrato.');
                    
                }
            })
            .then(blob => {
                if (blob) {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = `Contrato_${nomeCliente}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    
                    Swal.fire({
                        title: "Sucesso!",
                        text: "Comprovante gerado com sucesso.",
                        icon: "success"
                    
                        });

                    console.log("Contrato gerado");
                }
            })
            .catch(error => {
                console.error('Erro:', error);
            });
        } else {
            //alert("Operação cancelada.");
            console.log("Operação cancelada");
        }
    }
    );
}

function ficha() {

    var nomeCliente = document.getElementById("list").value; //get nome
    console.log(nomeCliente)
    var clienteId = document.querySelector("#my-list option[value='"+nomeCliente+"']").dataset.value; //id
    console.log(clienteId)

    Swal.fire({
        title: "Deseja gerar a ficha deste aluno?",
        text: "",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelButtonText: "Cancelar!",
        confirmButtonText: "Sim!"
        }).then((result) => {
        if (result.isConfirmed) {
        fetch(`/historico/ficha_generator/${clienteId}/`, {
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
                Swal.fire({
                    title: "Erro ao gerar a ficha.",
                    text: "Confira os dados do cadastro.",
                    icon: "warning"
                });
            }
        })
        .then(blob => {
            if (blob) {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `Ficha_${nomeCliente}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                

                Swal.fire({
                    title: "Sucesso!",
                    text: "Ficha gerada com sucesso.",
                    icon: "success"
                
                    });

                console.log("Ficha gerada");
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


