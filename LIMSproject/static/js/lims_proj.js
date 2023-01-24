const main = document.querySelector('main');
let btn_type_project = document.querySelector('.btn_type_project');
let btn_type_project2 = document.querySelector('.btn_type_project2');
let add_project_type1 = document.querySelector('.add_project_type1');
let add_project_type2 = document.querySelector('.add_project_type2');
let project_type_exit = document.querySelector('.fa-circle-xmark');
let project_exit = document.querySelector('.exit');
let retornar = document.querySelector('.return')

btn_type_project.addEventListener('click', select_project)

function select_project() {
    add_project_type1.classList.remove('inactive');
    main.style.opacity = '30%';

}

btn_type_project2.addEventListener('click', add_project)

function add_project() {
    add_project_type1.classList.add('inactive');
    add_project_type2.classList.remove('inactive');
    main.style.opacity = '30%';

}
project_type_exit.addEventListener('click', close_add_project_type)

function close_add_project_type() {
    add_project_type1.classList.add('inactive');
    main.style.opacity = '100%';
}

project_exit.addEventListener('click', close_add_project)

function close_add_project() {
    add_project_type2.classList.add('inactive');
    main.style.opacity = '100%';
}

retornar.addEventListener('click', retornar_project)

function retornar_project() {
    add_project_type2.classList.add('inactive')
    add_project_type1.classList.remove('inactive');
}