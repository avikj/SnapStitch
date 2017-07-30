var inter = setInterval(function(){
	var xhr = new XMLHttpRequest();

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			window.location.href = "www.google.com"
			clearInterval(inter)
		}
	});

	xhr.open("GET", "http://localhost:5000/file?groupid=test");

	xhr.send();
},5000);
