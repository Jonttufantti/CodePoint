console.log("Axios:", typeof axios);

function getData() {
    axios('http://data.foli.fi/siri/sm/672')
        .then(d=>createList(d.data.result))
}

function createList(stops) {
    const listEl = document.getElementById('stops-list')
    for (let stop of stops) {
        const el = document.createElement('li')
        const departureTime = new Date(parseInt(stop.expecteddeparturetime) * 1000 )
        const text = stop.lineref + ' ' + stop.destinationdisplay + ' ' + departureTime.toLocaleTimeString()
        el.innerHTML = text
        listEl.append(el)
    }
}