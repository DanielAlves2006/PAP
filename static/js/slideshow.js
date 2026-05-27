let index = 0;
let imagens = document.querySelectorAll(".slides img");

function mostrar() {
    for (let i = 0; i < imagens.length; i++) {
        imagens[i].style.display = "none";
    }

    imagens[index].style.display = "block";
}

function mudarSlide(n) {
    index += n;

    if (index >= imagens.length) {
        index = 0;
    }

    if (index < 0) {
        index = imagens.length - 1;
    }

    mostrar();
}

// iniciar
mostrar();