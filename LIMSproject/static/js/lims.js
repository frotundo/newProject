let elements_btn_service = document.querySelectorAll('#table-service .btn-service');

elements_btn_service.forEach(function(element){
    element.addEventListener('click', addParameters);
});
// btn_service.addEventListener('click', addParameters);

// document.addEventListener('click', addParameters);

function addParameters() {
    btn_service.classList.add('btn-service-active');

}

