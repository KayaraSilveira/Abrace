document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formRemoveMember');
    const btnConfirmRemoveMember = document.getElementById('btnConfirmRemoveMember');
    const modalButtonRemoveMember = document.getElementById('modalButtonRemoveMember');
  
    if (btnConfirmRemoveMember) {
        btnConfirmRemoveMember.addEventListener('click', function(event) {
            event.preventDefault();
            $('#confirmRemoveMemberModal').modal('show'); 
        });
    }
  
    if (modalButtonRemoveMember) {
        modalButtonRemoveMember.addEventListener('click', function() {
            form.submit();
        });
    }
  });
  