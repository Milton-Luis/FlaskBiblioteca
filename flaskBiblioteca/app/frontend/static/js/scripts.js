const submitBtn = document.querySelector(".submit-login");


// window.location.reload()



const checkNullForm = () =>{
	const inputs = document.querySelector(".checkInput");
	if(!(inputs.value)) return;
}

submitBtn.addEventListener("click", ()=>{
	checkNullForm();
})

// const add_book_btn = () =>{
// 	fetch("/registers", {
// 		headers:{
// 			'Content-Type' : 'application/json'
// 		},
// 		method: "GET",
// 		body: 
// 	});
// }
