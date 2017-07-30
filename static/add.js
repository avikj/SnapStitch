function run(){
	var input = document.querySelector('#vid-input')

	input.addEventListener('change', function(){
		var formData = new FormData()
		files = []
		for(var i=0;i<input.files.length;i++){
			formData.append('vidfiles',input.files[i])
		}
		var xhr = new XMLHttpRequest();
		xhr.withCredentials = true;

		xhr.addEventListener("readystatechange", function () {
		  if (this.readyState === 4) {
		  	var gid = JSON.parse(xhr.responseText)['groupid']
		  	url = "/loading/" + gid
		    window.location.href = url;
		  }
		});

		xhr.open("POST", "/upload");
		xhr.setRequestHeader("cache-control", "no-cache");
		xhr.setRequestHeader("postman-token", "066936fa-34af-fde5-da46-536332020ce8");

		xhr.send(formData);
		var overlay = document.querySelector('#overlay')
		overlay.style.display = "flex";
	});
};