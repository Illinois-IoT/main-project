let recordButton = document.getElementById("recordButton");
let recordButtonIcon = recordButton.firstElementChild;
let subtitle = document.getElementById("subtitle");

//add events to the button
recordButton.addEventListener("click", startListening);

function processResult(e) {
    //set the subtitle to the returned result
    subtitle.textContent = "Result: " + e.target.responseText;

    //show the microphone icon again
    recordButtonIcon.classList.replace("fa-circle", "fa-microphone");
    //re-enable the button
    recordButton.disabled = false;
}

function startListening() {
    //replace the microphone icon with a circle icon
    recordButtonIcon.classList.replace("fa-microphone", "fa-circle");
    //disable the button to prevent misclick
    recordButton.disabled = true;

    //set subtile to "listening..."
    subtitle.textContent = "Listening...";

    //send new GET request
    let xhr = new XMLHttpRequest();
    xhr.onload = processResult;
    xhr.open("GET", "listen", true);
    xhr.send();
}

