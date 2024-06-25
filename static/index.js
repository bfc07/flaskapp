function openForm() {
    document.getElementById("popup-window").style.display = "block";
}

function closeForm() {
    document.getElementById("popup-window").style.display = "none";
}

function validateForm() {
    var host = document.getElementById("host").value;
    if (host === "") {
        alert("Host field is required!");
        return false; // Prevent form submission
    }
    closeForm();
    return true; // Allow form submission
}