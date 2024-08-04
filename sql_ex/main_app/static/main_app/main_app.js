// Functions
function fetchRecordLabels() {
    fetch('/main_app/api/recordlabel/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const recordLabelDataDiv = document.getElementById('recordLabelData');
            recordLabelDataDiv.innerHTML = '';

            const table = document.createElement('table');
            const headerRow = document.createElement('tr');

            if (data.length > 0) {
                Object.keys(data[0]).forEach(key => {
                    const th = document.createElement('th');
                    th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
                    headerRow.appendChild(th);
                });
                table.appendChild(headerRow);

                data.forEach(record => {
                    const row = document.createElement('tr');
                    Object.values(record).forEach(value => {
                        const td = document.createElement('td');
                        td.textContent = value;
                        row.appendChild(td);
                    });
                    table.appendChild(row);
                });
            } else {
                recordLabelDataDiv.textContent = 'No record labels found.';
            }

            recordLabelDataDiv.appendChild(table);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// Event listeners
document.getElementById('fetchRecordLabels').addEventListener('click', fetchRecordLabels);
