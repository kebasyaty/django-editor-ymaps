ymaps.ready(function () {

    var Map,
        Placemark,
        $latitude = $('#id_latitude'),
        $longitude = $('#id_longitude'),
        coordinates = [parseFloat($latitude.val()), parseFloat($longitude.val())],
        coords;

    // Create map
    Map = new ymaps.Map("id_center_map", {
        center: coordinates,
        zoom: parseInt($('select#id_zoom option:selected').val())
    });

    $('#id_zoom').on('change', function() {
        Map.setZoom(parseInt($('select#id_zoom option:selected').val()));
    });

    Map.events.add('boundschange', function(e) {
        $('select#id_zoom option[value="' + e.get('target').getZoom() + '"]').prop('selected', true);
    });

    // Create placemark
    Placemark = new ymaps.Placemark(coordinates, {
        hintContent: '',
        balloonContent: ''
    }, {
        iconLayout: 'default#image',
        iconImageHref: '/static/yandex_maps/img/get_coord.png',
        iconImageSize: [45.0, 60.0],
        iconImageOffset: [-21.5, -58.0],
        draggable: true
    });

    Placemark.events.add('drag', function(e) {
        coords = e.get('target').geometry.getCoordinates();
        $latitude.val(coords[0]);
        $longitude.val(coords[1]);
    });

    Map.events.add('click', function(e){
        coords = e.get('coords');
        Placemark.geometry.setCoordinates(coords);
        $latitude.val(coords[0]);
        $longitude.val(coords[1]);
    });

    Map.geoObjects.add(Placemark);
});
