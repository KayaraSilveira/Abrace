document.addEventListener("DOMContentLoaded", function () {
    const filterSelect = document.getElementById("filterSelectProfile");
    const filterSelectView = document.getElementById("filterSelectProfileView");
    
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
    if (filterSelectView) {
        filterSelectView.addEventListener("change", function () {
            const selectedOption = filterSelectView.options[filterSelectView.selectedIndex].value;
            
            let url = window.location.pathname;
            url = url.substring(0, url.indexOf("/projects/") + "/projects/".length);

            // Adicione o filtro como um parâmetro na URL
            if (selectedOption !== 'Todos') {
                url += `filter/${selectedOption}`;
            }

            window.location.href = url;
        });
    }
});
