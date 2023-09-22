function validation() {
	var valid = true;
	var formLabels = document.getElementsByTagName("label");
  
	var firstName = document.signupForm.firstName.value;
	if (firstName === "") {
	  formLabels[0].innerHTML = "First Name: [Required]";
	  formLabels[0].style.color = "red";
	  valid = false;
	} else if (!isNaN(firstName)) {
	  formLabels[0].innerHTML = "First Name: [Text Only]";
	  formLabels[0].style.color = "red";
	  valid = false;
	} else {
	  formLabels[0].innerHTML = "First Name:";
	  formLabels[0].style.color = "black";
	  valid = valid ? true : false;
	}
  
	var lastName = document.signupForm.lastName.value;
	if (lastName === "") {
	  formLabels[1].innerHTML = "Last Name: [Required]";
	  formLabels[1].style.color = "red";
	  valid = false;
	} else if (!isNaN(lastName)) {
	  formLabels[1].innerHTML = "Last Name: [Text Only]";
	  formLabels[1].style.color = "red";
	  valid = false;
	} else {
	  formLabels[1].innerHTML = "Last Name:";
	  formLabels[1].style.color = "black";
	  valid = valid ? true : false;
	}
  
	var email = document.signupForm.email.value;
	var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (email === "") {
	  formLabels[2].innerHTML = "Email: [Required]";
	  formLabels[2].style.color = "red";
	  valid = false;
	} else if (!re.test(email)) {
	  formLabels[2].innerHTML = "Email: [Incorrect Email]";
	  formLabels[2].style.color = "red";
	  valid = false;
	} else {
	  formLabels[2].innerHTML = "Email:";
	  formLabels[2].style.color = "black";
	  valid = valid ? true : false;
	}
  
	var password = document.signupForm.password.value;
	if (password === "") {
	  formLabels[3].innerHTML = "Password: [Required]";
	  formLabels[3].style.color = "red";
	  valid = false;
	} else if (password.length < 4) {
	  formLabels[3].innerHTML = "Password: [Must be > 4]";
	  formLabels[3].style.color = "red";
	  valid = false;
	} else {
	  formLabels[3].innerHTML = "Password:";
	  formLabels[3].style.color = "black";
	  valid = valid ? true : false;
	}
  
	return valid;
  }
  
  function clear2() {
	var myArray = new Array();
	myArray[0] = "First Name: *";
	myArray[1] = "Last Name: *";
	myArray[2] = "Email: *";
	myArray[3] = "Password: *";
  
	var formLabels = document.getElementsByTagName("label");
	for (var i = 0; i < myArray.length; i++) {
	  formLabels[i].innerHTML = myArray[i];
	  formLabels[i].style.color = "black";
	}
  }
  