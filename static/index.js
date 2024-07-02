let inputs = [];

function addInput() {
    const host = document.getElementById('host').value.trim();
    const category = document.getElementById('category').value;

    if (host && category) {
        inputs.push({ host: host, category: category });
        displayInputs();
        document.getElementById('host').value = '';
        document.getElementById('category').value = '';
    } else {
        alert('Both fields are required');
    }
}

function displayInputs() {
    const table = document.getElementById('table');
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    inputs.forEach((input, index) => {
        const tr = document.createElement('tr');

        const tdHost = document.createElement('td');
        tdHost.textContent = input.host;
        tr.appendChild(tdHost);

        const tdCategory = document.createElement('td');
        tdCategory.textContent = input.category;
        tr.appendChild(tdCategory);

        const tdButton = document.createElement('td');
        const button = document.createElement('button');
        button.innerHTML = '&times;';
        button.onclick = function() { removeInput(index); };
        tdButton.appendChild(button);
        tr.appendChild(tdButton);

        table.appendChild(tr);
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