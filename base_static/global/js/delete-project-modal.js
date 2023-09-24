document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formDeleteProject');
    const btnConfirmDeleteProject = document.getElementById('btnConfirmDeleteProject');
    const modalButtonDeleteProject = document.getElementById('modalButtonDeleteProject');
  
    if (btnConfirmDeleteProject) {
        btnConfirmDeleteProject.addEventListener('click', function(event) {
        event.preventDefault();
        $('#confirmDeleteProjectModal').modal('show'); 
        });
    }
    
    if (modalButtonDeleteProject) {
        modalButtonDeleteProject.addEventListener('click', function() {
        form.submit();
        });
    }
  });
  