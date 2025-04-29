document.addEventListener('DOMContentLoaded', function () {
    // Registration Elements
    const registrationModal = document.getElementById('registrationModal');
    const registerBtn = document.getElementById('registerBtn');
    const regFormCloseBtn = document.getElementById('regFormCloseBtn');
    const registrationForm = document.getElementById('registrationForm');

    // Login Elements
    const loginModal = document.getElementById('loginModal');
    const loginBtn = document.getElementById('loginBtn');
    const loginFormCloseBtn = document.getElementById('loginFormCloseBtn');
    const loginForm = document.getElementById('loginForm');

    // Open registration modal
    registerBtn.addEventListener('click', function () {
        registrationModal.classList.remove('hidden');
    });

    // Close registration modal via X
    regFormCloseBtn.addEventListener('click', function () {
        registrationModal.classList.add('hidden');
    });

    // Close registration modal when clicking outside
    window.addEventListener('click', function (event) {
        if (event.target === registrationModal) {
            registrationModal.classList.add('hidden');
        }
    });

    // Registration form submission
    registrationForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const registrationUsername = document.getElementById('registrationUsername').value;
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const email = document.getElementById('email').value;
        const phoneNumber = document.getElementById('phoneNumber').value;
        const registrationPassword = document.getElementById('registrationPassword').value;

        try {
            const response = await fetch('/auth/sign-up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: registrationUsername,
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    phone_number: phoneNumber,
                    password: registrationPassword
                })
            });

            if (!response.ok) {
                throw new Error('Registration failed');
            }

            const data = await response.json();
            console.log('Registration successful:', data);

            registrationModal.classList.add('hidden');
            registrationForm.reset();
            alert('Registration successful!');
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed. Please try again.');
        }
    });

    // Open login modal
    loginBtn.addEventListener('click', function () {
        loginModal.classList.remove('hidden');
    });

    // Close login modal via X
    loginFormCloseBtn.addEventListener('click', function () {
        loginModal.classList.add('hidden');
    });

    // Close login modal when clicking outside
    window.addEventListener('click', function (event) {
        if (event.target === loginModal) {
            loginModal.classList.add('hidden');
        }
    });

    // Login form submission
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const loginUsername = document.getElementById('loginUsername').value;
        const loginPassword = document.getElementById('loginPassword').value;

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'username': loginUsername,
                    'password': loginPassword,
                    'grant_type': 'password'
                })
            });



            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            console.log('Login successful:', data);

            document.cookie = `access_token=${encodeURIComponent(data.access_token)}; Path=/; SameSite=Strict; Secure; Max-Age=${60 * 60 * 4}`;
            

            sessionStorage.setItem('User_id', data.user_id);


            loginModal.classList.add('hidden');
            loginForm.reset();
            alert('Login successful!');
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed. Please try again.');
        }
    });
});
