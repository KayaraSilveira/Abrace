document.addEventListener("DOMContentLoaded", function () {
    const zipcodeElement = document.getElementById("id_zipcode");

    zipcodeElement.addEventListener("focusout", (event) => {

        zipcode = event.target.value;

        zipcode = zipcode.replace("-", "");

        const url = 'https://viacep.com.br/ws/' + zipcode + '/json';

        request = new XMLHttpRequest();

        request.open('GET', url);
        request.onerror = (err) => {
            console.log("Erro ao buscar cep: " + err);

            cityElement = document.getElementById('id_city');
            cityElement.value = "";

            stateElement = document.getElementById('id_state');
            stateElement.value = "";

            countryElement = document.getElementById('id_country');
            countryElement.value = "";
        }
        request.onload = () => {
            const response = JSON.parse(request.responseText);

            if (response.erro == true) {
                console.log("cep não encontrado.");

                cityElement = document.getElementById('id_city');
                cityElement.value = "";

                stateElement = document.getElementById('id_state');
                stateElement.value = "";

                countryElement = document.getElementById('id_country');
                countryElement.value = "";
            } else {                
                cityElement = document.getElementById('id_city');
                cityElement.value = response.localidade;

                stateElement = document.getElementById('id_state');
                stateElement.value = response.uf;

                countryElement = document.getElementById('id_country');
                countryElement.value = "Brasil";
            }
        }

        request.send();
    })
})
