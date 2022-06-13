var recordButton = document.getElementById("recordButton");
var listeningButton = document.getElementById("listeningButton");

var subtitle = document.getElementById("subtitle");

//only display recordButton initially 
recordButton.style.display = "inline";
listeningButton.style.display = "none";

//add events to those 2 buttons
recordButton.addEventListener("click", startListening);

function processResult(e) {
    if (this.readyState === 4) {
        console.log("Server returned: ", e.target.responseText);
        subtitle.textContent = "Result: " + e.target.responseText;

        recordButton.style.display = "inline";
        listeningButton.style.display = "none";
    }
}

function startListening() {
    console.log("recordButton clicked");

    //hide the stop button, show the record to allow for new recordings
    recordButton.style.display = "none";
    listeningButton.style.display = "inline";

    subtitle.textContent = "Listening...";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = processResult;
    xhr.open("GET", "listen", true);
    xhr.send();
}

