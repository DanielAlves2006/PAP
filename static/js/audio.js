document.addEventListener('click', function () {
    var som = document.getElementById('meuSom');
    som.play().catch(function (error) {
        console.log("O autoplay foi bloqueado pelo navegador até o usuário interagir.");
    });
});

