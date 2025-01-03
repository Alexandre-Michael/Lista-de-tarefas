

/*Navbar menu and Navbar burger*/


document.addEventListener("DOMContentLoaded", () => {
	// Get all "navbar-burger" elements
	const $navbarBurgers = Array.prototype.slice.call(
		document.querySelectorAll(".navbar-burger"),
		0
	);

	// Add a click event on each of them
	$navbarBurgers.forEach((el) => {
		el.addEventListener("click", () => {
			// Get the target from the "data-target" attribute
			const target = el.dataset.target;
			const $target = document.getElementById(target);

			// Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
			el.classList.toggle("is-active");
			$target.classList.toggle("is-active");
		});
	});
});


/*Delete Pop-Up*/


function confirmDelete(event) {
	const userConfirmed = window.confirm(
		"Tem certeza que deseja excluir esta tarefa?"
	);
	if (!userConfirmed) {
		event.preventDefault(); // Cancela o envio do formulário se o usuário clicar em "Cancelar"
	}
	return userConfirmed; // Retorna true para continuar e enviar o formulário se "OK" for clicado.
}


/*Search Bar*/


document.getElementById('search-input').addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        const searchTerm = this.value.trim();
        window.location.href = `?search=${encodeURIComponent(searchTerm)}`;
    }
});