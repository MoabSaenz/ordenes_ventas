document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orden-form');
    const resetButton = document.getElementById('btn-reset');

    let skipConfirmSubmit = false;

    if (resetButton && form) {
        resetButton.addEventListener('click', () => {
            form.reset();
            const usuario = form.querySelector('input[name="usuario"]');
            if (usuario) usuario.focus();
        });
    }

    const confirmModalElement = document.getElementById('confirmModal');
    const confirmModalForm = document.getElementById('confirmModalForm');
    const confirmModalMessage = document.querySelector('.confirm-modal-message');
    const confirmModalAccept = document.querySelector('.confirm-modal-accept');
    let pendingForm = null;

    if (confirmModalElement && confirmModalForm && confirmModalMessage && confirmModalAccept) {
        const confirmModal = new bootstrap.Modal(confirmModalElement, {
            backdrop: 'static',
            keyboard: false,
        });

        document.querySelectorAll('form[data-confirm]').forEach((confirmFormElement) => {
            confirmFormElement.addEventListener('submit', (event) => {
                if (skipConfirmSubmit) {
                    skipConfirmSubmit = false;
                    return;
                }

                event.preventDefault();
                pendingForm = confirmFormElement;
                confirmModalMessage.textContent = confirmFormElement.dataset.confirm || '¿Desea continuar?';
                confirmModalAccept.textContent = 'Confirmar';
                confirmModalForm.action = '';
                confirmModal.show();
            });
        });

        document.querySelectorAll('.confirm-delete-btn').forEach((button) => {
            button.addEventListener('click', () => {
                pendingForm = null;
                confirmModalForm.action = button.dataset.action;
                confirmModalMessage.textContent = `¿Deseas eliminar la ${button.dataset.item}? Esta acción es irreversible.`;
                confirmModalAccept.textContent = 'Eliminar';
                confirmModal.show();
            });
        });

        confirmModalAccept.addEventListener('click', () => {
            if (pendingForm) {
                skipConfirmSubmit = true;
                pendingForm.submit();
            } else {
                confirmModalForm.submit();
            }
            confirmModal.hide();
        });
    }
});