function openPopup(){
    console.log("Popup opened");
    document.getElementById("loginPopup").style.display = "flex";
}

function closePopup(){
    document.getElementById("loginPopup").style.display = "none";
}

// click outside to close
window.onclick = function(event) {
    const popup = document.getElementById("loginPopup");
    if (event.target === popup) {
        popup.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function(){

    const form = document.getElementById("taskForm");

    if(form){

        form.addEventListener("submit", function(e){
            e.preventDefault();

            const formData = new FormData(form);

            fetch("/add/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {

                // Add new task to UI
                const taskList = document.querySelector(".task-list");

                const li = document.createElement("li");
                li.innerHTML = `
                    <span>${data.title} (${data.priority})</span>
                    <div>
                        <a href="/complete/${data.id}/">✔</a>
                        <a href="/delete/${data.id}/">❌</a>
                    </div>
                `;

                taskList.appendChild(li);

                form.reset();
            });
        });
    }
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}