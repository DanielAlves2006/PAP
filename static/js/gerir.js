document.addEventListener('DOMContentLoaded', function () {
    const selectAllCheckbox = document.getElementById('select-all');
    const productCheckboxes = document.querySelectorAll('.product-checkbox');
    const deleteButton = document.getElementById('btn-eliminar-selecionados');

    function updateDeleteButtonState() {
        const checkedCount = document.querySelectorAll('.product-checkbox:checked').length;
        deleteButton.disabled = (checkedCount === 0);

        if (checkedCount > 0) {
            deleteButton.textContent = `Eliminar Selecionados (${checkedCount})`;
        } else {
            deleteButton.textContent = 'Eliminar Selecionados';
        }

        if (checkedCount === 0) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
        } else if (checkedCount === productCheckboxes.length) {
            selectAllCheckbox.checked = true;
            selectAllCheckbox.indeterminate = false;
        } else {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = true;
        }
    }

    selectAllCheckbox.addEventListener('change', function () {
        productCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
        updateDeleteButtonState();
    });

    productCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateDeleteButtonState);
    });
});

