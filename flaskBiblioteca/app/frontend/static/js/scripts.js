// window.location.reload();
document.addEventListener("DOMContentLoaded", function () {
	const lock = () => {

		const password = document.querySelector("input[type='password']");
		const lockIcon = document.getElementById("lockUnlock");
		
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
});
document.addEventListener("DOMContentLoaded", function () {
	
	const add_zero = (num) => {
		return num >= 10 ? num : `0${num}`;
	};

	const format_date = (date) => {
		const day = date.getDate().toString().padStart(2, "0");
		const month = (date.getMonth() + 1).toString().padStart(2, "0");
		const year = date.getFullYear();
		
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
