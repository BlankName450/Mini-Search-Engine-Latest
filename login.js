function validation() {
	var valid = true;
	
	formLabels = document.getElementsByTagName("label");
	var email = document.loginForm.email.value;
	if(email==""){
		formLabels[0].innerHTML="Email: [Required]";
		formLabels[0].style="color: red";
		valid = false;
	}
	
	var password = document.loginForm.password.value;
	if(password == ""){
		formLabels[1].innerHTML="Password: [Required]";
		formLabels[1].style="color: red";
		valid = false;
	}

	return valid 
	
}

