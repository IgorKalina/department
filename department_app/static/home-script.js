
const baseURL = 'http://127.0.0.1:5000/api/';



getDepartmentsInfo = () => {
    const xhr = new XMLHttpRequest();
    let url_dep = baseURL + 'departments/';
    // find quantity of departments
    xhr.open('GET', url_dep, true)
    xhr.send(null)
    xhr.onload = function () {
    if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        document.querySelector('#departments').textContent = data.length;

        }
    }
}

getEmployeesInfo = () => {
    const xhr = new XMLHttpRequest();
    let url_emp = baseURL + 'employees/';
    // find quantity of departments
    xhr.open('GET', url_emp, true)
    xhr.send(null)
    xhr.onload = function () {
    if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        let emp_qty = data.length;
        let total_sum = 0;
        let total_average;
        for (let i=0; i < emp_qty; i++) {
            total_sum += data[i].salary;
        }
        if (emp_qty !== 0) {
            total_average = total_sum / emp_qty;
        } else {
            total_average = 0;
        }
        document.querySelector('#employees').textContent = emp_qty;
        document.querySelector('#salaries').textContent = Math.round(total_average) + '$';
        }
    }
}




getDepartmentsInfo();
getEmployeesInfo();


