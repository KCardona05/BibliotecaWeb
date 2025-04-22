// Eliminar Usuario
document.querySelectorAll('.btn-danger').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto (ir a la URL)

        const usuarioId = this.getAttribute('href').split('/').pop(); // Obtener el ID del usuario
        if (confirm("¿Estás seguro de que quieres eliminar este usuario?")) {
            fetch(`/admin/eliminar/${usuarioId}`, {
                method: 'GET', // Enviar solicitud GET para eliminar el usuario
            })
            .then(response => response.json()) // Parsear la respuesta JSON
            .then(data => {
                if (data.success) {
                    alert('Usuario eliminado exitosamente');
                    window.location.reload(); // Recargar la página para actualizar la lista
                } else {
                    alert(data.message); // Mostrar el mensaje de error
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error al realizar la solicitud');
            });
        }
    });
});

// Actualizar Usuario
function actualizarUsuario(usuarioId) {
    const updatedData = {
        nombre: document.querySelector('#nombre').value, // Obtener el valor del campo de nombre
        correo: document.querySelector('#correo').value, // Obtener el valor del campo de correo
        password: document.querySelector('#password').value, // Obtener el valor del campo de contraseña
        rol: document.querySelector('#rol').value, // Obtener el valor del campo de rol
    };

    fetch(`/admin/actualizar/${usuarioId}`, {
        method: 'POST', // Enviar solicitud POST para actualizar el usuario
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData), // Enviar los datos actualizados
    })
    .then(response => response.json()) // Parsear la respuesta JSON
    .then(data => {
        if (data.success) {
            alert('Usuario actualizado exitosamente');
            window.location.reload(); // Recargar la página
        } else {
            alert(data.message); // Mostrar el mensaje de error
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al realizar la solicitud');
    });
}
