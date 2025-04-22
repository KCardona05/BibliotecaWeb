// LOGIN
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('form-login');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(loginForm);
            const data = {
                txtemail: formData.get('txtemail'),
                txtpassword: formData.get('txtpassword')
            };

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    window.location.href = result.redirect_url;
                } else {
                    alert(result.message || "Error al iniciar sesión");
                }
            } catch (error) {
                console.error('Error:', error);
                alert("Error de conexión");
            }
        });
    }

    // REGISTRO
    const registerForm = document.getElementById('form-register');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(registerForm);
            const data = {
                txtname: formData.get('txtname'),
                txtemail: formData.get('txtemail'),
                txtpassword: formData.get('txtpassword'),
            };

            try {
                const response = await fetch('/registrar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    alert("Registro exitoso");
                    window.location.href = result.redirect_url;
                } else {
                    alert(result.message || "Error al registrar");
                }
            } catch (error) {
                console.error('Error:', error);
                alert("Error de conexión");
            }
        });
    }
});
