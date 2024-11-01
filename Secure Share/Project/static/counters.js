document.addEventListener("DOMContentLoaded", () => {
const usersCount = document.getElementById("users-count")
const filesCount = document.getElementById("files-count")
const sio = io.connect(location.protocol + '//' + document.domain + ':' + location.port)
sio.on("received_users_count", (data) => {
    usersCount.innerHTML = data
    setTimeout(()=>{sio.emit("get_users_count")}, 1000)
})
sio.on("received_files_count", (data) => {
    filesCount.innerHTML = data
    setTimeout(()=>{sio.emit("get_files_count")}, 1000)
})
setTimeout(()=>{sio.emit("get_users_count")}, 1000)
setTimeout(()=>{sio.emit("get_files_count")}, 1000)
})





