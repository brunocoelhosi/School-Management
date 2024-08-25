function exibir_form(tipo){

    sala1 = document.getElementById('sala1')
    sala2 = document.getElementById('sala2')

    if(tipo == "1"){
        sala2.style.display = "none"
        sala1.style.display = "block"

    }else if(tipo == "2"){
        sala1.style.display = "none";
        sala2.style.display = "block"
    }

}

$(function() {

    var $td = $("td");
  
    $td.on({
      "keypress" : function(e) {
        if (e.which !== 13) { // On Return key - "save" cell
          e.preventDefault();
          $(this).prop("contenteditable", false);
        }
      },
      "dblclick" : function() {
        $td.not(this).prop("contenteditable", false);
        $(this).prop("contenteditable", true);
      }
    });
  
  });
