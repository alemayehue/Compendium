function summarize() {
    if (document.getElementById('resultText').innerHTML == "Your processed summary will appear here.") {
        document.getElementById('resultText').innerHTML = "No valid input.";
        return;
    }

    // Clear the previous search
    document.getElementById('resultText').innerHTML = "Your processed summary will appear here.";

    // Get the user input from the text box
    let userInput = document.getElementById('userInput').value;

    // Send it to the Python server using a POST request
    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'user_input=' + userInput // Send the input as form data
    })
    .then(response => response.text())  // Get the response from the server
    .then(data => {
        // Display the response from Python in the 'resultText' section
        data = data.substring(1, data.length - 2);  // gets rid of beginning and end quote from jsonify
        document.getElementById('resultText').innerHTML = "";
        document.getElementById('resultText').innerHTML += data;
    });
}

function news() {
    if (document.getElementById('news').innerHTML == "Your relevant news articles will appear here.") {
        document.getElementById('news').innerHTML = "No valid input.";
        return;
    }

    // Clear the previous search
    document.getElementById('news').innerHTML = "Your relevant news articles will appear here.";

    let userInput = document.getElementById('userInput').value;

    // Send it to the Python server using a POST request
    fetch('/newskeywords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'user_input=' + userInput // Send the input as form data
    })
    .then(response => response.text())  // Get the response from the server
    .then(data => {
        // Display the response from Python in the 'news' section
        data = data.substring(0, data.length - 4);  // gets rid of beginning and end quote from jsonify
        document.getElementById('news').innerHTML = "No valid input.";
        document.getElementById('news').innerHTML += data;
    });
}

function research() {
    if (document.getElementById('research').innerHTML == "Your relevant research papers will appear here.") {
        document.getElementById('research').innerHTML = "";
        return;
    }

    // Clear the previous search
    document.getElementById('research').innerHTML = "Your relevant research papers will appear here.";

    let userInput = document.getElementById('userInput').value;

    // Send it to the Python server using a POST request
    fetch('/researchkeywords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'user_input=' + userInput // Send the input as form data
    })
    .then(response => response.text())  // Get the response from the server
    .then(data => {
        // Display the response from Python in the <div>
        data = data.substring(0, data.length - 4);  // gets rid of beginning and end quote
        document.getElementById('research').innerHTML = "";
        document.getElementById('research').innerHTML += data;
    });
}