//Registration

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('registrationModal');
    const registerBtn = document.getElementById('registerBtn');
    const closeBtn = document.getElementById('closeBtn');
    const registrationForm = document.getElementById('registrationForm');

    // Open modal when button is clicked
    registerBtn.addEventListener('click', function() {
        modal.classList.remove('hidden');
    });
    
    // Close modal with X button
    closeBtn.addEventListener('click', function() {
        modal.classList.add('hidden');
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    }); // <-- This parenthesis was missing in your code

    // Form submission handler
    registrationForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        // Get form values
        const username = document.getElementById('userName').value;
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const email = document.getElementById('email').value;
        const phoneNumber = document.getElementById('phoneNumber').value;
        const password = document.getElementById('password').value;
        

        //Send form data

        try {

            const response = await fetch('/auth/sign-up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    phone_number: phoneNumber,
                    password: password
                })

            });
            
            console.log(response)
            if (!response.ok) {
                throw new Error('Registration failed');
            }
    
            const data = await response.json();
            console.log('Registration successful:', data);
            
            // Close modal
            modal.classList.add('hidden');
            
            // Reset form
            registrationForm.reset();
    
            // Show success message to user
            alert('Registration successful!');
        
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed. Please try again.');
        }
    });

});