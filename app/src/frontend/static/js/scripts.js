// window.location.reload();
document.addEventListener( "DOMContentLoaded", function () {
	const calendar = () => {
		const day = document.querySelector( "#day" );
		const month = document.querySelector( "#month" );
		const monthText = new Date().toLocaleString( "pt-br", {
			month: "short",
		} ).replace( ".", "" );
		const dayNumber = new Date().toLocaleString( "default", {
			day: "2-digit",
		} );

		day.textContent = dayNumber;
		month.textContent = monthText;
	}
	calendar();
} );



document.addEventListener( "DOMContentLoaded", function () {
	const login = () => {
		const email = document.querySelector( "input[type='email']" );
		const password = document.querySelector( "input[type='password']" );
		const submit = document.querySelector( "input[type='submit']" );
		const lockIcon = document.getElementById( "lockUnlock" );

		const message = document.querySelector( "#message" );

		const category = "danger";
		submit.addEventListener( "click", ( event ) => {
			if ( email.value === "" || password.value === "" ) {
				event.preventDefault();
				let div = message.querySelector( "div" );
				if ( !div ) {
					div = document.createElement( "div" );
					div.classList.add( "alert", `alert-${category}` );
					div.textContent = "Preencha todos os campos!";
					message.appendChild( div );
				}
			}
		} );

		password.addEventListener( "input", () => {
			if ( password.value.length > 0 ) {
				lockIcon.classList.remove( "fa-unlock" );
				lockIcon.classList.add( "fa-lock" );
			} else {
				lockIcon.classList.remove( "fa-lock" );
				lockIcon.classList.add( "fa-unlock" );
			}
		} );
	};
	login();
} );
document.addEventListener( "DOMContentLoaded", function () {
	const add_zero = ( num ) => {
		return num >= 10 ? num : `0${num}`;
	};

	const format_date = ( date ) => {
		const day = date.getDate().toString().padStart( 2, "0" );
		const month = ( date.getMonth() + 1 ).toString().padStart( 2, "0" );
		const year = date.getFullYear();
		const hour = date.getHours().toString().padStart( 2, "0" );
		const minute = date.getMinutes().toString().padStart( 2, "0" );
		const second = date.getSeconds().toString().padStart( 2, "0" );

		return `${year}-${month}-${day}`;
		/**
		 * por padrão deve seguir essa configuração de retorno quando exibido num form, o navegador
		 * irá alterar o formato de data conforme a localidade em que esitver.
		 * Ex:Brasil - dd/mm/yyyy
		 *    Canada - mm/dd/yyyy
		 */
	};

	const date = new Date();
	const formated_date = format_date( date );

	document.querySelector( "#loan_date" ).value = formated_date;
} );

document.addEventListener( "DOMContentLoaded", () => {
	const searchInput = document.getElementById( "search" );
	const booksList = document.getElementById( "books-list" );

	searchInput.addEventListener( "input", () => {
		const query = searchInput.value;

		fetch( `/api/livros/search?q=${query}` )
			.then( ( response ) => response.text() )
			.then( ( data ) => {
				booksList.innerHTML = data;
			} )
			.catch( err => console.error( "Error fetching search results:", err ) );
	} );
} );

document.getElementById( "reader-form" ).addEventListener( "submit", ( e ) => {
	e.preventDefault();
} );

document.addEventListener( "DOMContentLoaded", function () {
	const searchInput = document.getElementById( "search" );
	const searchList = document.querySelector( "#search-list" );

	const urlParts = window.location.pathname.split( "/" );
	const slug = urlParts[urlParts.length - 2];

	let selectedName = "";

	searchInput.addEventListener( "input", () => {
		const query = searchInput.value.trim();

		if ( query === "" ) {
			searchList.innerHTML = "";
			return;
		}

		fetch( `/api/emprestimos/novo/${slug}/search?q=${query}` )
			.then( ( response ) => response.json() )
			.then( ( data ) => {
				searchList.innerHTML = "";

				if ( data.length === 0 ) {
					const noResults = document.createElement( "li" );
					noResults.classList.add( "mt-2", "pl-2" )
					noResults.textContent = "Nome não encontrado!";
					searchList.appendChild( noResults );
				} else {
					data.forEach( ( name ) => {
						const li = document.createElement( "li" );
						li.classList.add( "reader-name" );

						const nameParagraph = document.createElement( "p" );
						nameParagraph.textContent = `Nome: ${name.fullname}`;

						li.addEventListener( "click", () => {
							selectedName = name.fullname;
							searchInput.value = selectedName;

							fetch( "/api/emprestimos/selecionar-usuario", {
								method: "POST",
								headers: {
									"Content-Type": "application/json"
								},
								body: JSON.stringify( {
									reader_id: name.id
								} )
							} )
								.then( res => res.json() )
								.then( data => {
									if ( data.ok ) {
										console.log( "Usuário salvo na sessão" )
									}
								} );

							searchList.innerHTML = "";
						} );
						li.appendChild( nameParagraph );
						searchList.appendChild( li );
					} );
				}
			} );
	} );
} );


document.addEventListener( "DOMContentLoaded", function () {
	const toasts = document.querySelectorAll( ".toast" );

	toasts.forEach( toastEl => {
		const toast = new bootstrap.Toast( toastEl );
		toast.show();
	} );
} );