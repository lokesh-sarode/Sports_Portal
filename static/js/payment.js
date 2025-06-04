document.addEventListener("DOMContentLoaded", function (){
    
    const payButton = document.getElementById("pay-button");
    if(payButton){
        payButton.addEventListener("click", function(event) {
            event.preventDefault();

            // get the form data
            const full_name = document.getElementById("id_full_name")?.value.trim();
            const email = document.getElementById("id_email")?.value.trim();
            const college_name = document.getElementById("id_college_name")?.value.trim();
            const dept = document.getElementById("id_dept")?.value.trim();
            const year_of_study = document.getElementById("id_year_of_study")?.value.trim();
            const contact_number = document.getElementById("id_contact_number")?.value.trim();
            const emergency_contact = document.getElementById("id_emergency_contact")?.value.trim();

            const fees = parseFloat(document.getElementById("fees-value").textContent);
            const sub_event = payButton.getAttribute("data-sub-event"); 
        console.log(sub_event)
             // Validate inputs
            if (!full_name || !email || !college_name || !dept || !year_of_study || !contact_number || !emergency_contact) {
                alert("Please fill out all fields.");
                return;
            }

            if (!email.includes("@gmail.com")) {
                alert("Please enter a valid email address.");
                return;
            }

            if (contact_number.length < 10 || emergency_contact.length < 10 || contact_number.length > 12 || emergency_contact.length > 12) {
                alert("Please enter a valid phone number.");
                return;
            }

            // Get Fees
            if (isNaN(fees) || fees <= 0) {
                alert("Invalid fees amount. Please try again.");
                return;
            }

            
            // Get CSRF token from the hidden input field
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            //Razorpay payment integration
            const amountInPaise = fees * 100;  //razorpay requires the amount in paise
            const options = {
                key: "rzp_test_Am8Zi1bznoNdxl",
                amount: amountInPaise,
                currency: "INR",
                name: "GSMCOE Events",
                description: `${sub_event} Registration Payment`,                        
                handler: function(response){
                    // Send payment details to backend
                    fetch("/registration/success/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken,
                        },
                        body: JSON.stringify({
                            razorpay_payment_id: response.razorpay_payment_id,
                            name: full_name,
                            email: email,
                            college_name: college_name,
                            dept: dept,
                            year_of_study: year_of_study,
                            contact_number: contact_number,
                            emergency_contact: emergency_contact,
                            sub_event: sub_event,
                            fees: fees
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("Sub-Event:", sub_event); 
                        if (data.success) {
                            window.location.href = `/registration/success?payment_id=${response.razorpay_payment_id}`;
                        } else {
                            alert("Payment recorded, but an issue occurred while saving registration details.");
                        }
                    })
                    .catch(error => {
                        alert("Payment successful, but an error occurred. Please contact support.");
                        console.error("Error:", error);
                    });
                },
                prefill: {
                    name: full_name,
                    email: email,
                    phone: contact_number,
                },
                theme: {
                    color: "#d84e55",
                }
            }

            const rzp = new Razorpay(options);
            rzp.open();

            rzp.on("payment.failed", function(response){
                // handle payment failure
                alert("Payment failed. Please try again. Error: " + response.error.description)
            })

        })
    }
        
})
