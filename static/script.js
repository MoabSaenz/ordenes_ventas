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

    // Details modal population
    document.addEventListener('DOMContentLoaded', function () {
        var detailsModal = document.getElementById('detailsModal');
        if (!detailsModal) return;
            var cachedDetailsHtml = document.getElementById('detailsBody') ? document.getElementById('detailsBody').innerHTML : null;
            // restore original details on modal hide
            detailsModal.addEventListener('hidden.bs.modal', function () {
                var body = document.getElementById('detailsBody');
                if (body && cachedDetailsHtml) body.innerHTML = cachedDetailsHtml;
                var footer = detailsModal.querySelector('.modal-footer');
                if (footer) footer.innerHTML = '<a id="d-edit-btn" class="btn btn-primary" href="#">Editar</a><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>';
            });

        detailsModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            if (!button) return;
            // restore default footer (in case previous edit replaced it)
            var footer = detailsModal.querySelector('.modal-footer');
            if (footer) {
                footer.innerHTML = '<a id="d-edit-btn" class="btn btn-primary" href="#">Editar</a><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>';
            }
            var oid = button.getAttribute('data-id') || '';
            var numero = button.getAttribute('data-numero') || '';
            var usuario = button.getAttribute('data-usuario') || '';
            var fecha = button.getAttribute('data-fecha') || '';
            var fecha_factura = button.getAttribute('data-fecha-factura') || '';
            var fecha_termino = button.getAttribute('data-fecha-termino') || '';
            var factura = button.getAttribute('data-factura') || '';
            var estatus = button.getAttribute('data-estatus') || '';
            var descripcion = button.getAttribute('data-descripcion') || '';
            var comentarios = button.getAttribute('data-comentarios') || '';
            var pdf = button.getAttribute('data-pdf') || '';

            document.getElementById('d-numero').textContent = numero;
            document.getElementById('d-usuario').textContent = usuario;
            document.getElementById('d-fecha').textContent = fecha || '-';
            document.getElementById('d-fecha-factura').textContent = fecha_factura || '-';
            document.getElementById('d-fecha-termino').textContent = fecha_termino || '-';
            document.getElementById('d-factura').textContent = factura || '-';
                // show estatus as colored badge
                var estNode = document.getElementById('d-estatus');
                if (estNode) {
                    if (estatus === 'completo') estNode.innerHTML = '<span class="badge bg-success">Completo</span>';
                    else if (estatus === 'proceso') estNode.innerHTML = '<span class="badge bg-warning text-dark">En proceso</span>';
                    else if (estatus === 'pendiente') estNode.innerHTML = '<span class="badge bg-secondary">Pendiente</span>';
                    else estNode.textContent = estatus || '-';
                }
            document.getElementById('d-descripcion').textContent = descripcion || '-';
            document.getElementById('d-comentarios').textContent = comentarios || '-';
            var pdfNode = document.getElementById('d-pdf');
            if (pdf) {
                pdfNode.innerHTML = '<a href="' + pdf + '" target="_blank" rel="noopener">Ver PDF</a>';
            } else {
                pdfNode.textContent = '-';
            }
            // set edit link
            var editBtn = document.getElementById('d-edit-btn');
            if (editBtn) {
                if (oid) {
                    editBtn.href = '/editar/' + oid + '/';
                    editBtn.style.display = '';
                } else {
                    editBtn.style.display = 'none';
                }
            }
            // Edit-in-modal: load form fragment and handle submit via AJAX
            if (editBtn) {
                editBtn.addEventListener('click', function (e) {
                    if (!oid) return;
                    e.preventDefault();
                    fetch('/editar_modal/' + oid + '/')
                        .then(function (resp) { return resp.text(); })
                        .then(function (html) {
                            // replace details body with form
                            var body = document.getElementById('detailsBody');
                            body.innerHTML = html;
                            // Replace footer buttons: show Save and Cancel
                            var footer = detailsModal.querySelector('.modal-footer');
                            footer.innerHTML = '';
                            var saveBtn = document.createElement('button');
                            saveBtn.type = 'button';
                            saveBtn.className = 'btn btn-primary';
                            saveBtn.textContent = 'Guardar';
                            var cancelBtn = document.createElement('button');
                            cancelBtn.type = 'button';
                            cancelBtn.className = 'btn btn-secondary';
                            cancelBtn.setAttribute('data-bs-dismiss', 'modal');
                            cancelBtn.textContent = 'Cancelar';
                            footer.appendChild(saveBtn);
                            footer.appendChild(cancelBtn);

                            // handle save click -> submit form via fetch
                            saveBtn.addEventListener('click', function () {
                                var form = document.getElementById('modal-edit-form');
                                if (!form) return;
                                var formData = new FormData(form);
                                fetch(form.action, {
                                    method: 'POST',
                                    body: formData,
                                    credentials: 'same-origin'
                                }).then(function (r) {
                                    if (r.ok) {
                                        // close modal and reload to reflect changes
                                        var bsModal = bootstrap.Modal.getInstance(detailsModal);
                                        bsModal.hide();
                                        window.location.reload();
                                    } else {
                                        return r.json().then(function (j) { alert(j.error || 'Error al guardar'); });
                                    }
                                }).catch(function (err) { alert('Error: ' + err); });
                            });
                        }).catch(function (err) { alert('No se pudo cargar el formulario: ' + err); });
                }, { once: true });
            }
        });
    });