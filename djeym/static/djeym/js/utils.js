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
