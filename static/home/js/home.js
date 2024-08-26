
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
