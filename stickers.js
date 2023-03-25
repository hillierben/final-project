// timestable check answer

function check() {
    let x = document.querySelector('#answer').value;
    if (x == "Ambulance") {
        document.querySelector('#answer').style.backgroundColor = "green";
        document.querySelector('#answer').value = "CORRECT";
    }
    else {
        document.querySelector('#answer').style.backgroundColor = "red";
        document.querySelector('#answer').value = "WRONG";
    }
}