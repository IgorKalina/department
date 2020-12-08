const delButton = document.querySelector('.delete-btn');
const xhr = new XMLHttpRequest();
let baseURL = 'http://127.0.0.1:5000/';
let baseAPI = baseURL + 'api/';
let url;
let _id;
let redirect_url;


if (window.location.pathname.includes('department')) {
    url = baseAPI + 'department/'
    _id = window.location.pathname[12];
    redirect_url = baseURL + 'departments'

} else {
    url = baseAPI + 'employee/'
    _id = window.location.pathname[10];
    redirect_url = baseURL + 'employees';
}


delButton.addEventListener('click', function () {

    let conf = confirm('Delete Item?');
    console.log(conf);
    if (conf) {
            xhr.open('DELETE', url + _id, true)
            //xhr.setRequestHeader('Access-Control-Allow-Origin','*')
            xhr.send(null)
            xhr.onload = function () {
            if (xhr.status === 200) {
            window.location.replace(redirect_url);
            alert(xhr.responseText)
            }
        }
    }
})





