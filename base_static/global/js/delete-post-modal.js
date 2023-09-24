document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    
    deleteButtons.forEach(function(button) {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        console.log('aquie');
        
        const formId = this.parentElement.id; 
        console.log(formId)
        const modalId = `#confirmDeletePost${formId}Modal`; 
        
        $(modalId).modal('show'); 
        
        const confirmButton = document.querySelector(`${modalId} .btn-confirm`);
        
        if (confirmButton) {
          confirmButton.addEventListener('click', function() {
            const form = document.getElementById(formId); 
            form.submit(); 
          });
        }
      });
    });
  });
  