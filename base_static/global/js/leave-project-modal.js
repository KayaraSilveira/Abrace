document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formLeaveProject');
    const btnConfirmLeave = document.getElementById('btnConfirmLeave');
    const modalButtonLeave = document.getElementById('modalButtonLeave');
  
    if(btnConfirmLeave) {
      btnConfirmLeave.addEventListener('click', function(event) {
      event.preventDefault();
        $('#confirmLeaveModal').modal('show'); 
      });
    }
  
    if(modalButtonLeave) {
      modalButtonLeave.addEventListener('click', function() {
        form.submit();
      });
    }
  });
  