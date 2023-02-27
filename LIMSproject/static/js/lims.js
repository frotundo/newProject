let elements_btn_service = document.querySelectorAll('#table-service .btn-service');
let btn_add_service = document.querySelector('.btn_add_service');
let add_service_type = document.querySelector('.add_service_type');
let service_exit = document.querySelector('.exit-service');
const main = document.querySelector('main');
// let btn_add_model = document.querySelector('.btn_add_model');
// let add_model_service_type = document.querySelector('.add_model_service_type');
// let model_exit = document.querySelector('.exit-model');


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

// btn_add_model.addEventListener('click', add_model)

// function add_model() {
//     add_model_service_type.classList.remove('inactive');
//     main.style.opacity = '30%';

// }

// model_exit.addEventListener('click', close_add_model)

// function close_add_model() {
//     add_model_service_type.classList.add('inactive');
//     main.style.opacity = '100%';
// }
