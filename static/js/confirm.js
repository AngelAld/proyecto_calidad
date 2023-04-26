$(function () {
  $('.eliminar_form').on('submit', function (event) {
    console.log('SI ESTÁ CARGANDO EL SCRIPT')
    var $target = $(event.target);
    if ($target.hasClass('eliminar_btn')) {
      event.preventDefault();
      swal({
        title: "¿Estás seguro?",
        text: "Una vez eliminado, no podrás recuperar este semestre.",
        icon: "warning",
        buttons: ["Cancelar", "Eliminar"],
        dangerMode: true,
    })
    .then((willDelete) => {
        if (willDelete) {
        }
    });
    }
  });
});

