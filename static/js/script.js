document.addEventListener("DOMContentLoaded", () => {

	// Menu Navbar

	document.addEventListener("click", (event) => {
		const target = event.target;
		if (target.classList.contains("navbar-burger")) {
			const menu = document.getElementById(target.dataset.target);
			target.classList.toggle("is-active");
			menu.classList.toggle("is-active");
		}
	});

	// Barra de Pesquisa

	const searchInput = document.getElementById("search-input");
	if (searchInput) {
		searchInput.addEventListener("keyup", (event) => {
			if (event.key === "Enter") {
				const searchTerm = searchInput.value.trim();
				if (searchTerm) {
					window.location.href = `?search=${encodeURIComponent(
						searchTerm
					)}`;
				}
			}
		});
	}

	// File Input

	const fileInput = document.querySelector(
		"#file-js-example input[type=file]"
	);
	if (fileInput) {
		fileInput.addEventListener("change", () => {
			if (fileInput.files.length > 0) {
				document.querySelector(
					"#file-js-example .file-name"
				).textContent = fileInput.files[0].name;
			}
		});
	}

	// Confirmação de ações

	document.addEventListener("click", (event) => {
        const target = event.target.closest("[data-confirm]"); // Garante que funciona em elementos internos também
        if (target) {
            const message = target.getAttribute("data-confirm");
            if (!window.confirm(message)) {
                event.preventDefault();
                event.stopPropagation(); // Impede que o evento continue se o usuário cancelar
            }
        }
    });
});