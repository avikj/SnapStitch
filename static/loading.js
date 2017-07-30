function run(gid){
	var inter = setInterval(function(){
		var xhr = new XMLHttpRequest();

		xhr.addEventListener("readystatechange", function () {
			if (this.readyState === 4) {
				window.location.href = "/" + gid
				clearInterval(inter)
			}
		});

		xhr.open("GET", "/file?groupid=" + gid);

		xhr.send();
	},5000);
}
