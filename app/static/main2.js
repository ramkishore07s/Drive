// get data from /getFiles and display them
// add on click methods for all of them

var open_file = function(file) {
    return function() {
	window.open("/getfile/" + file);
    };
}

var change_folder = function(folder) {
    return function() {
	cd(folder);
    };
};

var fill_in_files = function(data, id) {
    list = document.getElementById(id);
    list.innerHTML = "";
    for(var i=0; i<data.length; ++i) {
	li = document.createElement('li');
	li.appendChild(document.createTextNode(data[i]));
	list.appendChild(li);
	li.onclick = open_file(data[i])
    }
};

var fill_in_sizes = function(data, id) {
    list = document.getElementById(id);
    list.innerHTML = "";
    for(var i=0; i<data.length; ++i) {
	li = document.createElement('li');
	li.appendChild(document.createTextNode(data[i]));
	list.appendChild(li);
    }
};

var fill_in_folders = function(data, id) {
    list = document.getElementById(id);
    list.innerHTML = "";
    for(var i=0; i<data.length; ++i) {
	li = document.createElement('li');
	li.appendChild(document.createTextNode(data[i]));
	list.appendChild(li);
	li.onclick = change_folder(data[i]);
    }
};

var ls = function() {
    var xhr = new XMLHttpRequest();
    var url = "/getFiles";
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
	if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
//            console.log(json);
//	    console.log(json.files);
	    fill_in_files(JSON.parse(json.files), "files");
	    fill_in_folders(JSON.parse(json.folders), "folders");
	    fill_in_sizes(JSON.parse(json.file_size), "file_sizes");
	}
    };
    xhr.send();
};

var cd = function(folder) {
    var xhr = new XMLHttpRequest();
    var url = "/changedir";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
	if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
	    
	    ls();
	}
    };
    var data = JSON.stringify({"change_dir":folder});
    xhr.send(data);
};

ls();

var delete_file = function(file) {
    var xhr = new XMLHttpRequest();
    var url = "/delete";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
	if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
	    
	    ls();
	}
    };
    var data = JSON.stringify({"del_file":file});
    xhr.send(data);
};
