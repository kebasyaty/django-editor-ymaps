function get_coordinates(address, lat_selector, long_selector) {
    utilsYMaps.geocode(address)
        .then(function (res) {
            var coords = res.geoObjects.get(0).geometry.getCoordinates();
            $(lat_selector).html(coords[0]);
            $(long_selector).html(coords[1]);
        });
}

function get_distance(point1, point2, object_selector) {
    // Расчет расстояния
    // Координаты 1
    utilsYMaps.geocode(point1)
        .then(function (res) {
            var firstCoords = res.geoObjects.get(0)
                .geometry.getCoordinates();
            // Координаты 2
            utilsYMaps.geocode(point2)
                .then(function (res) {
                    var secondCoords = res.geoObjects.get(0)
                        .geometry.getCoordinates();
                    // Расстояние
                    var distance = utilsYMaps.formatter.distance(utilsYMaps.coordSystem.geo.getDistance(
                        firstCoords, secondCoords));
                    $(object_selector).html(distance);
                });
        });
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    let R = 6371; // Radius of the earth in km
    let dLat = deg2rad(lat2 - lat1);  // deg2rad below
    let dLon = deg2rad(lon2 - lon1);
    let a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)
    ;
    let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    let d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180)
}

utilsYMaps.ready(init);

function relateSuggests(preselector="") {
    var suggests = new Array();
    $(preselector + "input[type=text][mode=suggest]").each(function () {
        suggests.push(new utilsYMaps.SuggestView(this, {
                results: 1,
                zIndex: 90000,
            }));
        $(this).attr("suggest-id", suggests.length - 1);
    });
    $(preselector + "input[type=text][mode=suggest]").on("change", function () {
        let suggest = suggests[$(this).attr("suggest-id")];
        let dataManager = suggest.state;
        dataManager.singleSet("activeIndex", 0);
        this.dispatchEvent(new KeyboardEvent('keydown', {'keyCode':13, 'which':13}));
        $(this).change();
        /*let first_item = dataManager.get('items')[0];
        $(this).val(first_item.value);
        //this.value = first_item.value;
        $(this).trigger("blur");
        //this.dispatchEvent(new KeyboardEvent('keydown', {'keyCode':27, 'which':27}));*/
    });
}

function relateCitySuggests(preselector="") {
    var suggests = new Array();
    $(preselector + "input[type=text][mode=citysuggest]").each(function () {
        suggests.push(new utilsYMaps.SuggestView(this, {
                provider: cityprovider,
                results: 1,
                zIndex: 90000,
            }));
        $(this).attr("suggest-id", suggests.length - 1);
    });
    $(preselector + "input[type=text][mode=citysuggest]").on("change", function () {
        let suggest = suggests[$(this).attr("suggest-id")];
        let dataManager = suggest.state;
        dataManager.singleSet("activeIndex", 0);
        this.dispatchEvent(new KeyboardEvent('keydown', {'keyCode':13, 'which':13}));
        $(this).change();
    });
}

function relateCityRegionSuggests(preselector="") {
    var suggests = new Array();
    $(preselector + "input[type=text][mode=cityregionsuggest]").each(function () {
        suggests.push(new utilsYMaps.SuggestView(this, {
                provider: cityregionprovider,
                results: 2,
                zIndex: 90000,
            }));
        $(this).attr("suggest-id", suggests.length - 1);
    });
    $(preselector + "input[type=text][mode=cityregionsuggest]").on("change", function () {
        let suggest = suggests[$(this).attr("suggest-id")];
        let dataManager = suggest.state;
        let items = dataManager.get('items');
        if (items.length === 1) {
            dataManager.singleSet("activeIndex", 0);
            this.dispatchEvent(new KeyboardEvent('keydown', {'keyCode': 13, 'which': 13}));
            $(this).change();
        }
    });
}


function init() {
    relateSuggests();
    relateCitySuggests();
    relateCityRegionSuggests();
}