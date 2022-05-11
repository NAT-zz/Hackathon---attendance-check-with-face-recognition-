var myStudentAPI = 'http://localhost:3000/student'
var myClassAPI = 'http://localhost:3000/class'
var myAttendAPI = 'http://localhost:3000/attendance'


function start() {
    
    window.onload = function() { 
        var buttonElementStudent = document.getElementById('add')
        buttonElementStudent.onclick = e => {
            getStudents(renderStudents)

        }
        // buttonElementStudent.onclick = e => {

        // }

        // if (buttonElementText === 'Save')
        //     updateData()
        // handleAdding()
    }
}
start()

// Fucntions
function getStudents(callback) {
    fetch(myStudentAPI)
    .then(function(res){
        return res.json()
    })
    .then(callback)
}
function renderStudents(data) {
    var html = ''
    listCourses = data
    data.forEach(element => {
        html += `
        <div class="item">
            <div class="item-details">
                <img class="item-pic" src="{{ url_for('static', filename = 'styles/assets/admin/layout3/img/avatar4.jpg') }}">
                <a href="" class="item-name primary-link">${element.name} - ${element.id}</a>
            </div>
            <span class="item-status"><span class="badge badge-empty badge-success"></span> Available</span>
        </div>
        `
    });
    console.log(html)
    document.getElementById('allStudent').innerHTML = html
}
// function handleAdding() {
//     document.querySelector('#add') .onclick = function(e)  {
//         var nameElement = document.querySelector('input[name="name"]').value
//         var homeElement = document.querySelector('input[name="description"]').value

//         var newCourse = {
//             name : nameElement,
//             description : homeElement
//         }
//         sendCourse(newCourse, function(data) {
//             document.getElementById('list-courses').innerHTML += 
//             `
//             <li>
//                 <h2>${data.name}</h2>
//                 <p>${data.description}</p>
//                 <button onclick = "handleDeleteCourse(${data.id})">Delete</button>
//                 <button onclick = "handleLoadData(${data.id})">Load</button>
//             </li>
//             `
//         })
//     }
// }
// function sendCourse(newCourse, callback) {
//     fetch(myAPI, {
//         method: 'POST',
//         headers : {
//             'Content-type' : 'application/json'
//         },
//         body: JSON.stringify(newCourse)
//     }).then(function (res) {
//         return res.json()
//     }).then(callback)
// }
// function handleDeleteCourse(courseId){
//     fetch(myAPI + "/" + courseId, {
//         method: 'DELETE',
//     })
//     .then(function() {
//         getCourses(renderListCourse)
//          // nên chọc vào DOM để xóa chứ không nên render lại page
//     })
// }
// function handleLoadData(id) {
//     getCourses(function(courses) {
//         var course =  courses.find(function(course, index) {
//             return course.id == id
//         })

//         if (course.name)
//             document.querySelector("input[name='name']").value = course.name
//         if (course.description)
//             document.querySelector("input[name='description']").value = course.description
//     })

//     document.getElementById('add').innerText = 'Save'
//     updateData(id)
// }

// function updateData(id) {
//     var buttonElementText = document.getElementById('add').innerText  
//     if (buttonElementText === 'Save')
//     {
//         document.getElementById('add').onclick = function(e) {
//             var courseName = document.querySelector('input[name = "name"]').value
//             var courseDes = document.querySelector('input[name = "description"]').value

//             fetch(myAPI + "/" + id, 
//             {
//                 method : 'PUT',
//                 headers : {
//                     'Content-type' : 'application/json'
//                 },
//                 body: JSON.stringify({
//                     name : courseName,
//                     description : courseDes  
//                 })
//             })
//             .then(function (course){
//                 return course.json()
//             })

//             location.reload()
//         }
//     }
// }