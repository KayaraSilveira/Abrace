let photo = document.getElementById('imgPhoto');
let file = document.getElementById('flImage');

if (photo) {
    photo.addEventListener('click', () => {
        file.click();
    });
}

if (file){
    file.required = false;
    file.addEventListener('change', () => {

        if (file.files.length <= 0) {
            return;
        }

        let reader = new FileReader();

        reader.onload = () => {
            photo.src = reader.result;
        }

        reader.readAsDataURL(file.files[0]);
    });

}