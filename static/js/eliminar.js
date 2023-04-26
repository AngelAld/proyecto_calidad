async function eliminar(formulario) {
    console.log('Si entramos al script')
    const id = formulario.querySelector('input[name="id"]').value;


    const result = await Swal.fire({
        title: '¿Estás seguro?',
        text: 'Esta acción no se puede recuperar',
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: 'NO',
        confirmButtonText: 'SI',
        reverseButtons: true
    });

    if (result.isConfirmed) {
        // Envía el formulario
        formulario.submit();
    }
};