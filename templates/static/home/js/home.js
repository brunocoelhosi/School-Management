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