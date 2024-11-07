function getTilat() {
    axios.get('/tilat')
        .then(response => createList(response.data))
        .catch(error => console.error("Error fetching tilat:", error));
}

function createList(tilat) {
    const listEl = document.getElementById('tilat-list');
    listEl.innerHTML = '';
    tilat.forEach(tila => {
        const el = document.createElement('li');
        el.innerHTML = `ID: ${tila.id}, Nimi: ${tila.tilan_nimi}`;
        listEl.appendChild(el);
    });
}
