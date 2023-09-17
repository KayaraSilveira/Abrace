document.addEventListener("DOMContentLoaded", function () {
    const filterSelect = document.getElementById("filterSelect");
    
    if (filterSelect) {
        filterSelect.addEventListener("change", function () {
            const selectedOption = filterSelect.options[filterSelect.selectedIndex].value;
            
            let url = '/accounts/profile/projects';

            // Adicione o filtro como um parâmetro na URL
            if (selectedOption !== 'Todos') {
                url += `/filter/${selectedOption}`;
            }

            window.location.href = url;
        });
    }
});
