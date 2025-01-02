////Fechar navbar ao clicar fora dela
document.addEventListener('click', function(event) {
    var navbarCollapse = document.getElementById('navbarNav');
    var isClickInsideNavbar = navbarCollapse.contains(event.target);
    var isNavbarToggler = document.querySelector('.navbar-toggler').contains(event.target);

    if (!isClickInsideNavbar && !isNavbarToggler && navbarCollapse.classList.contains('show')) {
        var bsCollapse = new bootstrap.Collapse(navbarCollapse);
        bsCollapse.hide();
    }
});

/////// Fechar a navbar ao selecionar uma das opções de menu
document.querySelectorAll('.navbar-nav .nav-link, .scrollToCard').forEach(function(navLink) {
    navLink.addEventListener('click', function() {
        var navbarCollapse = document.getElementById('navbarNav');
        if (navbarCollapse.classList.contains('show')) {
            var bsCollapse = new bootstrap.Collapse(navbarCollapse);
            bsCollapse.hide();
        }
    });
});


/////Evento para centralizar ao selecionar opcao
// Seleciona todos os links com a classe "scrollToCard"
const buttons = document.querySelectorAll('.scrollToCard');

// Adiciona o evento de clique para cada botão
buttons.forEach(button => {
  button.addEventListener('click', function(event) {
    event.preventDefault(); // Prevenir o comportamento padrão do link
    
    // Seleciona o card de matrícula
    const card = document.getElementById('cardmat');
    
    // Faz o scroll até o card centralizando-o
    card.scrollIntoView({
      behavior: 'smooth', // Suaviza o movimento de rolagem
      block: 'center'     // Centraliza o card verticalmente
    });
  });
});

////////evento da section cursos
document.addEventListener('DOMContentLoaded',() => {
    new TypeIt('.animated',{

        speed:200,
        loop: true,

    })

    .type('Crianças', {delay:700})
    .delete(9)
    .type('Jovens',{delay:700})
    .delete(6)
    .type('Adultos',{delay:700})
    .delete(7)
    .type('3ª Idade',{delay:700})
    .delete(8)
    .pause(100)
    .go();

});

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

document.addEventListener('DOMContentLoaded', (event) => {

    document.getElementById('novaMatricula').addEventListener('submit', function(e) {
        e.preventDefault();
        const cardName = document.getElementById('cardName').value;
        const cardEmail = document.getElementById('cardEmail').value;
        const cardFone = document.getElementById('cardFone').value;
        const cardNascimento = document.getElementById('cardNascimento').value;

        fetch('/nova_matricula/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                cardName: cardName,
                cardEmail : cardEmail,
                cardFone: cardFone,
                cardNascimento: cardNascimento,

            
            })
        })
        .then(response => {
            if (response.ok) {
                
                Swal.fire({
                    title: "Pré-matricula realizada com sucesso!",
                    text: "Entraremos em contato para conclusão da matricula.",
                    icon: "success"
                  });
                
            } else {
                console.error('Erro ao enviar os dados.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    });
});
