const lock = () => {
	let password = document.querySelector("input[type='password']");
	let lockIcon = document.getElementById("lockUnlock");

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
lock();

const submitBtn = document.querySelector(".submit-login");

// window.location.reload()

const checkNullForm = () => {
	const inputs = document.querySelector(".checkInput");
	if (!inputs.value) return;
};

submitBtn.addEventListener("click", () => {
	checkNullForm();
});

// const displayCurrentDate =() =>{
// 	const currentDate = Date.now();
// 	const currentMonth
// }
