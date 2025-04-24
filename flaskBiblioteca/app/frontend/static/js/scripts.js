// window.location.reload();
document.addEventListener("DOMContentLoaded", function () {
	const removeMessage = () => {
		const message = document.querySelector("#message");
		const div = message.querySelector("div");
		if (div) {
			setTimeout(() => {
				message.removeChild(div);
			}, 2000);
		}
	};
	removeMessage();
});

document.addEventListener("DOMContentLoaded", function () {
	const login = () => {
		const email = document.querySelector("input[type='email']");
		const password = document.querySelector("input[type='password']");
		const submit = document.querySelector("input[type='submit']");
		const lockIcon = document.getElementById("lockUnlock");

		const message = document.querySelector("#message");

		const category = "danger";
		submit.addEventListener("click", (event) => {
			if (email.value === "" || password.value === "") {
				event.preventDefault();
				let div = message.querySelector("div");
				if (!div) {
					div = document.createElement("div");
					div.classList.add("alert", `alert-${category}`);
					div.textContent = "Preencha todos os campos!";
					message.appendChild(div);
				}
			}
		});

		password.addEventListener("input", () => {
			if (password.value.length > 0) {
				lockIcon.classList.remove("fa-unlock");
				lockIcon.classList.add("fa-lock");
			} else {
				lockIcon.classList.remove("fa-lock");
				lockIcon.classList.add("fa-unlock");
			}
		});
	};
	login();
});
document.addEventListener("DOMContentLoaded", function () {
	const add_zero = (num) => {
		return num >= 10 ? num : `0${num}`;
	};

	const format_date = (date) => {
		const day = date.getDate().toString().padStart(2, "0");
		const month = (date.getMonth() + 1).toString().padStart(2, "0");
		const year = date.getFullYear();
		const hour = date.getHours().toString().padStart(2, "0");
		const minute = date.getMinutes().toString().padStart(2, "0");
		const second = date.getSeconds().toString().padStart(2, "0");

		return `${year}-${month}-${day}`;
		/**
		 * por padrão deve seguir essa configuração de retorno quando exibido num form, o navegador
		 * irá alterar o formato de data conforme a localidade em que esitver.
		 * Ex:Brasil - dd/mm/yyyy
		 *    Canada - mm/dd/yyyy
		 */
	};

	const date = new Date();
	const formated_date = format_date(date);

	document.querySelector("#lending_date").value = formated_date;
});

document.addEventListener("DOMContentLoaded", function () {
	const searchInput = document.getElementById("search");
	const booksList = document.getElementById("books-list");

	searchInput.addEventListener("input", function () {
		const query = searchInput.value;

		fetch(`/api/livros/search?q=${query}`)
			.then((response) => response.json())
			.then((data) => {
				booksList.innerHTML = "";
				data.forEach((book) => {
					const li = document.createElement("li");
					li.classList.add("h-56", "w-36", "border");

					const link = document.createElement("a");
					link.href = `/livros/detalhes/${book.title}`;
					link.textContent = book.title;

					li.appendChild(link);
					booksList.appendChild(li);
				});
			});
	});
});

document.addEventListener("DOMContentLoaded", function () {
	const searchInput = document.getElementById("search");
	const searchList = document.querySelector("#search-list");

	const urlParts = window.location.pathname.split("/");
	const bookTitle = urlParts[urlParts.length - 2];

	let selectedName = "";

	searchInput.addEventListener("input", function () {
		const query = searchInput.value.trim();

		if (query === "") {
			searchList.innerHTML = "";
			return;
		}

		fetch(`/api/emprestimos/novo/${bookTitle}/search?q=${query}`)
			.then((response) => response.json())
			.then((data) => {
				searchList.innerHTML = "";

				if (data.length === 0) {
					const noResults = document.createElement("li");
					noResults.classList.add("mt-2", "pl-2")
					noResults.textContent = "Nome não encontrado!";
					searchList.appendChild(noResults);
				} else {
					data.forEach((name) => {
						const li = document.createElement("li");
						li.classList.add(
							"cursor-pointer",
							"hover:bg-slate-500",
							"hover:text-white",
							"py-2",
							"pl-2",
							"border",
							"border-slate-400",
							"w-full",
							"flex",
							"justify-start",
							"gap-8",
							"first:mt-2"
							
						);
						const nameParagraph = document.createElement("p");
						const infoParagraph = document.createElement("p");

						const infoText = name.info.length > 0 ? name.info[0].info : "Sem informação";

						nameParagraph.textContent = `Nome: ${name.fullname}`;
						infoParagraph.textContent = `${infoText}`;

						li.addEventListener("click", () => {
							selectedName = name.fullname;
							setTimeout(() => {
								searchInput.value = selectedName;
							}, 10);
							searchList.innerHTML = "";
						});
						li.appendChild(nameParagraph);
						li.appendChild(infoParagraph);
						searchList.appendChild(li);
					});
				}
			});
	});
});
