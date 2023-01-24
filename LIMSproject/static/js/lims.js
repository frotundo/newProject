let elements_btn_service = document.querySelectorAll('#table-service .btn-service');
let btn_add_service = document.querySelector('.btn_add_service');
let add_service_type = document.querySelector('.add_service_type');
let service_exit = document.querySelector('.fa-circle-xmark');
const main = document.querySelector('main');


elements_btn_service.forEach(function(element){
    element.addEventListener('click', addParameters);
});

function addParameters() {
    btn_service.classList.add('btn-service-active');

}

btn_add_service.addEventListener('click', add_service)

function add_service() {
    add_service_type.classList.remove('inactive');
    main.style.opacity = '30%';

}

service_exit.addEventListener('click', close_add_service)

function close_add_service() {
    add_service_type.classList.add('inactive');
    main.style.opacity = '100%';
}
