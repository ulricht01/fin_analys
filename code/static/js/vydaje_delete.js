fetch('/vydaje_tabulka_data')
    .then(response => response.json())
    .then(data => {
        vytvorTabulku(data);
    })
    .catch(error => {
        console.error('Chyba při získávání dat:', error);
    });

function vytvorTabulku(data) {
    var container = document.getElementById("tabulka-container");
    var table = document.createElement("table");

    // Vytvoření záhlaví tabulky
    var headerRow = table.insertRow();
    for (var key in data) {
        var headerCell = document.createElement("th");
        headerCell.textContent = key.charAt(0).toUpperCase() + key.slice(1);
        headerRow.appendChild(headerCell);
    }
    // Přidání hlavičky pro tlačítka "Akce"
    var headerCellAction = document.createElement("th");
    headerCellAction.textContent = "Akce";
    headerRow.appendChild(headerCellAction);

    // Vytvoření řádků tabulky z hodnot datového objektu
    for (var i = 0; i < data.ids.length; i++) {
        var row = table.insertRow();
        for (var key in data) {
            var cell = row.insertCell();
            cell.textContent = data[key][i];
        }
        // Přidání tlačítka "Smazat" do každého řádku
        var cellAction = row.insertCell();
        var deleteButton = document.createElement("button");
        deleteButton.textContent = "Smazat";
        deleteButton.dataset.id = data.ids[i]; // Přidání atributu data-id s ID záznamu
        deleteButton.addEventListener("click", function(event) {
            var id = event.target.dataset.id;
            smazatZaznam(id); // Zavolání funkce pro smazání záznamu
        });
        cellAction.appendChild(deleteButton);
    }

    container.appendChild(table);
}

function smazatZaznam(id) {
    fetch(`/smazat_vydaj_zaznam/${id}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            throw new Error("Chyba při mazání záznamu");
        }
    })
    .catch(error => {
        console.error("Chyba při mazání záznamu:", error);
    });
}