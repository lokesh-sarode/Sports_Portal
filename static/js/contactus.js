document.addEventListener("DOMContentLoaded", function(){
   
    const submitButton = document.getElementById("submit")
    if(submitButton){
        submitButton.addEventListener("click", function(event) {
            event.preventDefault();

            const name = document.getElementById("name")?.value.trim();
            const email = document.getElementById("email")?.value.trim();
            const message = document.getElementById("message")?.value.trim();
            console.log(name, email, message)
            if(!name || !email || !message){
                alert("Please fill out all fields.");
                return;
            }
            if (!email.includes("@gmail.com")) {
                alert("Please enter a valid email address.");
                return;
            }
            alert("Your request has been sent to the admin..!")
            window.location.href = '/';
        })
    }     
    })