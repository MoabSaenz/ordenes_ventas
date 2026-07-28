document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orden-form');
    const resetButton = document.getElementById('btn-reset');

    if (form) {
        form.addEventListener('submit', () => {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Guardando...';
            }
        });
    }

    if (resetButton && form) {
        resetButton.addEventListener('click', () => {
            form.reset();
            const usuario = form.querySelector('input[name="usuario"]');
            if (usuario) usuario.focus();
        });
    }
});