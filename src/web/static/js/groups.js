
$(function () {
  /* Functions */
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-group .modal-content").html("");
        
        $("#modal-group").modal("show");
        
      },
      success: function (data) {
        $("#modal-group .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
 
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {

          $("#book-table tbody").html(data.html_group_list);
          if (data.vm_start){
            alert("VM is starting");  
          }

          if (data.vm_stop){
            alert("VM is stopping");  
          }

          if (data.vm_restart){
            alert("VM is restarting");  
          }
          if (data.schedule){
            alert("Schedule information is saved");
          }


          
          
          
          $("#modal-group").modal("hide");
        }
        else {
          alert("form is invalid. Please refresh the page")
          $("#modal-group .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-group").click(loadForm);
  $("#modal-group").on("submit", ".js-group-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-group", loadForm);
  $("#modal-group").on("submit", ".js-group-update-form", saveForm);
  
  // Delete book
  $("#book-table").on("click", ".js-delete-group", loadForm);
  $("#modal-group").on("submit", ".js-group-delete-form", saveForm);

});
