const deshacer = document.getElementById("deshacer");
const formulario = document.getElementById("formulario");

deshacer.addEventListener("click", () => {
    formulario.reset();
});