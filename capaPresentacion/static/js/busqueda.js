function buscar_semestre() {
  var input = document.getElementById("busqueda");
  var filter = input.value.toLowerCase();
  var table = document.getElementById("tabla");
  var rows = table.getElementsByTagName("tr");

  if (filter == "") {
    // Si el cuadro de búsqueda está vacío, mostrar todos los semestres
    for (var i = 0; i < rows.length; i++) {
      rows[i].style.display = "";
    }
  } else {
    // Buscar semestres que contengan la cadena de búsqueda
    for (var i = 0; i < rows.length; i++) {
      var nombre = rows[i].getElementsByTagName("td")[1];
      if (nombre) {
        var text = nombre.innerHTML.toLowerCase();
        if (text.indexOf(filter) > -1) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
      }
    }
  }
}

