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
        // Use default Bootstrap behavior so backdrop and ESC close the modal correctly
        const confirmModal = new bootstrap.Modal(confirmModalElement);

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

// Initialize DataTables for all tables (5 rows per page, ordering enabled)
if (window.jQuery) {
    (function($){
        $(function(){
            if ($.fn && $.fn.dataTable) {
                $('table.datatable').each(function(){
                    if (!$.fn.DataTable.isDataTable(this)) {
                        $(this).DataTable({
                            pageLength: 5,
                            lengthChange: false,
                            ordering: true,
                            language: {
                                url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
                            }
                        });
                    }
                });
            }
        });
    })(jQuery);
}