let inputs = [];

function addInput() {
    const field1 = document.getElementById('field1').value;
    const field2 = document.getElementById('field2').value;

    if (field1 && field2) {
        inputs.push({ field1, field2 });
        displayInputs();
        document.getElementById('field1').value = '';
        document.getElementById('field2').value = '';
    } else {
        alert('Both fields are required');
    }
}

function displayInputs() {
    const inputList = document.getElementById('inputList');
    inputList.innerHTML = '';
    inputs.forEach((input, index) => {
        const li = document.createElement('li');
        const div = document.createElement('div');
        div.className = 'input-content';
        div.innerHTML = `${input.field1} <br/><br/> ${input.field2}`;
        
        const button = document.createElement('button');
        button.innerHTML = '&times;';
        button.onclick = function() { removeInput(index); };
        
        li.appendChild(div);
        li.appendChild(button);
        inputList.appendChild(li);
    });
}



function removeInput(index) {
    inputs.splice(index, 1);
    displayInputs();
}


async function submitForm() {
    if (inputs.length > 0) {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ inputs }),
        });
        document.getElementById('inputList').innerHTML = '';
        inputs = [];

    } else {
        alert('Please add at least one input');
    }
}