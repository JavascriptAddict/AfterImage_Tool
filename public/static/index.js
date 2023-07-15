var map = L.map('map').setView([1.3521, 103.8198], 13);
var markers = new Array();
var proxyDataTable = "";
var pendingDataTable = "";

$(document).ready(function () {
    proxyDataTable = $('#proxyTable').DataTable({
        ajax: {
            url: 'http://127.0.0.1:5000/proxies',
            dataSrc: 'proxies'
        },
        columns: [
            {data: 'ip'},
            {data: 'port'},
            {data: 'country'},
            {data: 'https'},
            {data: 'lat'},
            {data: 'lng'},
            {data: 'connState'},
            {data: 'timeLastChecked'}
        ]
    });
    pendingDataTable = $('#pendingTable').DataTable({
        ajax: {
            url: 'http://127.0.0.1:5000/attacksawait',
            dataSrc: 'attacks'
        },
        columns: [
            {data: 'uid'},
            {data: 'srcaddr'},
            {data: 'srcport'},
            {data: 'dstaddr'},
            {data: 'attack'},
            {data: ''},
        ],
        columnDefs: [
            {
                targets: -1,
                data: null,
                defaultContent: '<button type="button" class="btn btn-success">Confirm</button>',
            },
        ],
    });
    attackDataTable = $('#attackTable').DataTable({
        ajax: {
            url: 'http://127.0.0.1:5000/attacks',
            dataSrc: 'attacks'
        },
        columns: [
            {data: 'uid'},
            {data: 'srcaddr'},
            {data: 'srcport'},
            {data: 'dstaddr'},
            {data: 'attack'},
        ],
    });
    $('#pendingTable tbody').on('click', 'button', function () {
        var data = pendingDataTable.row($(this).parents('tr')).data();
        console.log(data)
        fetch(`http://127.0.0.1:5000/test?uid=${data["uid"]}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
        });
        
    });
    setInterval(function () {
        proxyDataTable.ajax.reload(); 
        pendingDataTable.ajax.reload(); 
        attackDataTable.ajax.reload(); 
    }, 3000);
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

function capitalize(string){
    str = string.toLowerCase().replace(/\b[a-z]/g, function(letter) {
        return letter.toUpperCase();
    });
    return str
}

async function getProxies(){
    const response = await fetch('http://127.0.0.1:5000/proxies');
    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);
    }
    const proxies = await response.json();
    return proxies;
}

function proxyPage(){
    $("#pendingTableDiv").hide();
    $("#attackTableDiv").hide();
    $("#mapTitle").show();
    $("#map").show();
    getProxies().then(data => {
        proxies = data.proxies;
        for (let i = 0; i < proxies.length; i++){
            proxy = proxies[i];
            var marker = L.marker([proxy.lat, proxy.lng]);
            marker.bindPopup(`<b>${proxy.ip}:${proxy.port}</b>
            <p>Country: ${proxy.country} (${proxy.countryCode})</p>
            <p>HTTPS: ${proxy.https}</p>
            <p>Conn State: ${proxy.connState}</p>
            <p>Location: ${proxy.lat}, ${proxy.lng}</p>
            <p>Last Checked: ${proxy.timeLastChecked}</p>
            `).openPopup(map);
            map.addLayer(marker);
            markers.push(marker);
        } 
        $("#proxyTableDiv").show();
        // proxyDataTable.ajax.reload(); 
    })
    .catch(error => {
        alert(error.message);
    });
}

function removeMarkers(){
    for(i = 0; i < markers.length; i++) {
        map.removeLayer(markers[i]);
    }  
}

function attacksPage(){
    $("#proxyTableDiv").hide();
    $("#pendingTableDiv").hide();
    $("#mapTitle").show();
    $("#map").show();
    $("#attackTableDiv").show();
    removeMarkers();
}

function pendingPage(){
    $("#proxyTableDiv").hide();
    $("#attackTableDiv").hide();
    $("#mapTitle").hide();
    $("#map").hide();
    $("#pendingTableDiv").show();
    // pendingDataTable.ajax.reload(); 
}
