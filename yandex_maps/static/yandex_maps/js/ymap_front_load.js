ymaps.ready(function () {

    if (!window.center_ymap) return false;

    var Map,
        global_collections = {
            polyline: {},
            polygon: {}
        },
        global_cluster,
        global_placemarks = [],
        global_tmp,
        global_placemarks_length = 0,
        global_bool_all_category_filter = true,
        global_bool_not_all_category_filter = true,
        global_bool_collections = true;


    if (window.cluster_custom_icon_ymap !== null) {
        global_cluster = new ymaps.Clusterer({
            zoomMargin: 60,
            clusterIcons: [{
                href: window.cluster_custom_icon_ymap,
                size: window.cluster_size_ymap,
                offset: window.cluster_offset_ymap
            }],
            clusterIconContentLayout: null
        });
    } else {
        global_cluster = new ymaps.Clusterer({
            preset: window.cluster_icon_ymap,
            zoomMargin: 60
        });
    }


    // Создаем карту----------------------------------------------------------------------------------------------------

    Map = new ymaps.Map('id_ymap', {
        center: window.center_ymap,
        zoom: window.zoom_ymap
    }, {hintCloseTimeout: null});

    Map.events.add('balloonopen', function () {
        Map.hint.close();
    });


    // Выбор по категориям----------------------------------------------------------------------------------------------

    // ожидаем переключения polyline-polygon all
    function waitAll($all, bool_checked) {
        if (!$all.is(':checked') === bool_checked) {
            setTimeout(function () {
                waitAll($all, bool_checked);
            }, 100);
        } else {
            if ($all.attr('name') === 'placemark') {
                global_bool_not_all_category_filter = true;
            } else {
                global_bool_collections = true;
            }
            return false;
        }
    }

    function changeCollection(pk, name, action) {

        if (pk !== 'all') {

            var $switch_ymap_item_collection = $('.switch_ymap_item_collection[name="' + name + '"]:checked').not('[value="all"]'),
                $all = $('.switch_ymap_item_collection[name="' + name + '"][value="all"]');

            global_collections[name][parseInt(pk)].options.set('visible', action);

            if ($('.switch_ymap_item_collection[name="' + name + '"]').not('[value="all"]').length ===
                $switch_ymap_item_collection.length) {

                if (!$all.is(':checked')) {
                    global_bool_collections = false;
                    $all.parent().find('span.switchery > small').trigger('click');
                    waitAll($all, true);
                }

            } else if ($switch_ymap_item_collection.length === 0) {

                if ($all.is(':checked')) {
                    global_bool_collections = false;
                    $all.parent().find('span.switchery > small').trigger('click');
                    waitAll($all, false);
                }
            }

        } else {

            var collections = global_collections[name];

            for (var key in collections) {
                collections[key].options.set('visible', action);
            }

            if (action) {

                global_bool_collections = false;

                $('.switch_ymap_item_collection[name="' + name + '"]').not(':checked, [value="all"]').each(function () {
                    $(this).parent().find('span.switchery > small').trigger('click');
                });

            } else {

                global_bool_collections = false;

                $('.switch_ymap_item_collection[name="' + name + '"]:checked').not('[value="all"]').each(function () {
                    $(this).parent().find('span.switchery > small').trigger('click');
                });
            }

            global_bool_collections = true;
        }
    }

    function changeAllCategoryAndFilter(action) {

        var index;

        if (action) {
            for (index = 0; index < global_placemarks_length; index++)
                global_cluster.add(global_placemarks[index]);
        } else {
            for (index = 0; index < global_placemarks_length; index++)
                global_cluster.remove(global_placemarks[index]);
        }

        if (action) {

            $('.switch_ymap_item_collection[name="placemark"]').not(':checked, [value="all"]').each(function () {
                $(this).parent().find('span.switchery > small').trigger('click');
            });

            $('.switch_ymap_item_collection[name="submark"]:checked').each(function () {

                $(this).parent().find('span.switchery > small').trigger('click');
            });

        } else {

            $('.switch_ymap_item_collection[name="placemark"]:checked, ' +
                '.switch_ymap_item_collection[name="submark"]:checked').not('[value="all"]').each(function () {

                $(this).parent().find('span.switchery > small').trigger('click');
            });
        }

        global_bool_all_category_filter = true;
    }

    function changeCategoryAndFilter() {

        var index;

        var category_ids = [],
            filter_ids = [],
            filter_ids_length,
            $switch_ymap_item_collection = $('.switch_ymap_item_collection[name="placemark"]:checked').not('[value="all"]'),
            $all =  $('.switch_ymap_item_collection[name="placemark"][value="all"]');

        $switch_ymap_item_collection.each(function () {
            category_ids.push(parseInt($(this).val()));
        });

        $('.switch_ymap_item_collection[name="submark"]:checked').each(function () {
            filter_ids.push(parseInt($(this).val()));
        });

        filter_ids_length = filter_ids.length;

        if (filter_ids_length > 0) {

            for (index = 0; index < global_placemarks_length; index++) {
                global_tmp = global_placemarks[index];

                if ($(global_tmp.properties.get('collectionID')).filter(category_ids).get().length &&
                    $(global_tmp.properties.get('subCollectionIDs')).filter(filter_ids).get().length === filter_ids_length) {

                    global_cluster.add(global_tmp);
                } else {
                    global_cluster.remove(global_tmp);
                }
            }
        } else {

            for (index = 0; index < global_placemarks_length; index++) {
                global_tmp = global_placemarks[index];

                if ($(global_tmp.properties.get('collectionID')).filter(category_ids).get().length) {

                    global_cluster.add(global_tmp);
                } else {
                    global_cluster.remove(global_tmp);
                }
            }
        }

        if ($('.switch_ymap_item_collection[name="placemark"]').not('[value="all"]').length ===
            $switch_ymap_item_collection .length) {

            if (!$all.is(':checked')) {
                global_bool_not_all_category_filter = false;
                $all.parent().find('span.switchery > small').trigger('click');
                waitAll($all, true);
            }

        } else if ($switch_ymap_item_collection .length === 0) {

            if ($all.is(':checked')) {
                global_bool_not_all_category_filter = false;
                $all.parent().find('span.switchery > small').trigger('click');
                waitAll($all, false);
            }
        }

        global_tmp = null;
    }

    // Загрузка геообъектов---------------------------------------------------------------------------------------------

    // добавить линии из ajax ответа
    function addPolyline(polylines) {

        var Polyline,
            count = polylines.length,
            tmp,
            fields,
            collection_id;

        global_tmp = global_collections['polyline'];
        for (var i = 0; i < count; i++) {

            tmp = polylines[i];
            fields = tmp['fields'];
            collection_id = fields['category'];

            Polyline = new ymaps.Polyline($.evalJSON(fields['coordinates']), {
                hintContent: fields['hint_content'],
                balloonContentHeader: fields['hint_content'],
                balloonContentBody: fields['balloon_content'],
                pk: tmp['pk'],
                collectionID: collection_id
            }, {
                strokeWidth: fields['stroke_width'],
                strokeColor: fields['stroke_color'],
                strokeOpacity: parseFloat(fields['stroke_opacity'])
            });

            // линию в коллекцию
            global_tmp[collection_id].add(Polyline);
        }
        global_tmp = null;
    }

    // добавить полигоны из ajax ответа
    function addPolygon(polygons) {

        var Polygon,
            count = polygons.length,
            tmp,
            fields,
            collection_id;

        global_tmp = global_collections['polygon'];
        for (var i = 0; i < count; i++) {

            tmp = polygons[i];
            fields = tmp['fields'];
            collection_id = fields['category'];

            Polygon = new ymaps.Polygon($.evalJSON(fields['coordinates']), {
                hintContent: fields['hint_content'],
                balloonContentHeader: fields['hint_content'],
                balloonContentBody: fields['balloon_content'],
                pk: tmp['pk'],
                collectionID: collection_id
            }, {
                strokeWidth: fields['stroke_width'],
                strokeColor: fields['stroke_color'],
                strokeOpacity: parseFloat(fields['stroke_opacity']),
                fillColor: fields['fill_color'],
                fillOpacity: parseFloat(fields['fill_opacity'])
            });

            // полигон в коллекцию
            global_tmp[collection_id].add(Polygon);
        }
        global_tmp = null;
    }

    // добавить метки из ajax ответа
    function addPlacemark(placemarks) {
        var Placemark,
            count = placemarks.length,
            tmp,
            fields,
            collection_id,
            icon_name,
            custom_icon;

        for (var i = 0; i < count; i++) {

            tmp = placemarks[i];
            fields = tmp['fields'];
            collection_id = fields['category'];
            icon_name = fields['icon_name'];

            if (icon_name.search('#') > -1) {
                if (icon_name.search('Stretchy') == -1) {

                    Placemark = new ymaps.Placemark($.evalJSON(fields['coordinates']), {
                        hintContent: fields['hint_content'],
                        balloonContentHeader: fields['icon_content'],
                        balloonContentBody: fields['balloon_content'],
                        pk: tmp['pk'],
                        collectionID: collection_id,
                        subCollectionIDs: fields['subcategory'],
                        IconName: icon_name
                    }, {
                        preset: icon_name,
                        iconColor: fields['color']
                    });

                } else {

                    Placemark = new ymaps.Placemark($.evalJSON(fields['coordinates']), {
                        iconContent: fields['icon_content'],
                        hintContent: fields['hint_content'],
                        balloonContentHeader: fields['icon_content'],
                        balloonContentBody: fields['balloon_content'],
                        pk: tmp['pk'],
                        collectionID: collection_id,
                        subCollectionIDs: fields['subcategory'],
                        IconName: icon_name
                    }, {
                        preset: icon_name
                    });
                }

            } else {

                custom_icon = window.custom_icons_ymap[icon_name];

                Placemark = new ymaps.Placemark($.evalJSON(fields['coordinates']), {
                    hintContent: fields['hint_content'],
                    balloonContentHeader: fields['icon_content'],
                    balloonContentBody: fields['balloon_content'],
                    pk: tmp['pk'],
                    collectionID: collection_id,
                    subCollectionIDs: fields['subcategory'],
                    IconName: icon_name
                }, {
                    iconLayout: 'default#image',
                    iconImageHref: custom_icon[0],
                    iconImageSize: custom_icon[1],
                    iconImageOffset: custom_icon[2]
                });
            }

            // метку в коллекцию
            global_placemarks.push(Placemark);
        }

        global_cluster.add(global_placemarks);
        Map.geoObjects.add(global_cluster);
    }

    // AJAX-------------------------------------------------------------------------------------------------------------

    // Общая загрузка геообъектов
    $(function () {
        $.get(
            '/yandex_maps/load_geoobjects/',
            {id_map: window.id_ymap},
            function (data) {
                if (data['success']) {

                    var collections = data['collections'],
                        geoobjects,
                        $select_collection,
                        collection,
                        count,
                        tmp,
                        pk,
                        Collection,
                        index,
                        fields,
                        key,
                        // switchery
                        flag_first_switchs = true,
                        elems,
                        switchery,
                        // settings switchery - https://github.com/abpetkov/switchery
                        defaults = {
                                color: '#82cdff'
                                , secondaryColor: '#dfdfdf'
                                , jackColor: '#fff'
                                , jackSecondaryColor: null
                                , className: 'switchery'
                                , disabled: false
                                , disabledOpacity: 0.5
                                , speed: '0.4s'
                                , size: 'small'
                        };

                    // добавить коллекции полилиний, полигонов и меток
                    for (key in collections) {

                        collection = $.evalJSON(collections[key]);
                        count = collection.length;

                        if (key === 'placemark') {
                            $select_collection = $('#id_ymap_list_collection_placemark').find('fieldset').eq(0);

                            for (index = 0; index < count; index++) {
                                tmp = collection[index];
                                pk = tmp['pk'];
                                fields = tmp['fields'];
                                $select_collection.append('<p><input type="checkbox" class="switch_ymap_item_collection" ' +
                                    'checked name="placemark" value="' + pk + '" /><span class="ymap_title_collection">' +
                                    fields['title'] + '</span></p>');
                            }
                        } else if (key ==='submark') {
                            $select_collection = $('#id_ymap_list_collection_placemark').find('fieldset').eq(1);

                            for (index = 0; index < count; index++) {
                                tmp = collection[index];
                                pk = tmp['pk'];
                                $select_collection.append('<p><input type="checkbox" class="switch_ymap_item_collection" ' +
                                    'name="submark" value="' + pk + '" /><span class="ymap_title_collection">' +
                                    tmp['fields']['title'] + '</span></p>');
                            }
                        } else {
                            $select_collection = $('#id_ymap_list_collection_' + key);

                            for (index = 0; index < count; index++) {
                                tmp = collection[index];
                                pk = tmp['pk'];
                                $select_collection.append('<p><input type="checkbox" class="switch_ymap_item_collection" ' +
                                    'checked name="' + key + '" value="' + pk + '" /><span class="ymap_title_collection">' +
                                    tmp['fields']['title'] + '</span></p>');

                                Collection = new ymaps.GeoObjectCollection({},{visible: true});
                                global_collections[key][pk] = Collection;
                                Map.geoObjects.add(Collection);
                            }
                        }
                    }

                    collections
                        = collection
                        = $select_collection
                        = Collection = null;

                    geoobjects = data['geoobjects'];
                    data = null;

                    // добавить метки в коллекции
                    tmp = $.evalJSON(geoobjects['placemarks']);
                    geoobjects['placemarks'] = null;
                    if (tmp.length) {
                        addPlacemark(tmp);
                        global_placemarks_length = global_placemarks.length;
                    }

                    // добавить полилинии в коллекци
                    tmp = $.evalJSON(geoobjects['polylines']);
                    geoobjects['polylines'] = null;
                    if (tmp.length) {
                        addPolyline(tmp);
                    }

                    // добавить полигоны в коллекции
                    tmp = $.evalJSON(geoobjects['polygons']);
                    geoobjects = null;
                    if (tmp.length) {
                        addPolygon(tmp);
                    }

                    // Запускается фильтр коллекций
                    elems = Array.prototype.slice.call(document.querySelectorAll('.switch_ymap_item_collection'));
                    $(elems).each(function (index, element) {
                        var $this = $(element);

                        if ($this.val() !== 'all') {
                            switchery = new Switchery(element, defaults);
                        } else {
                            switchery = new Switchery(element, {color: '#56db40', size: 'small'});
                        }
                        element.onchange = function() {

                            switch ($this.attr('name')) {
                                case 'polyline':
                                    // Смена коллекций
                                    if (global_bool_collections)
                                        changeCollection($this.val(), 'polyline', element.checked);
                                    break;
                                case 'polygon':
                                    // Смена коллекций
                                    if (global_bool_collections)
                                        changeCollection($this.val(), 'polygon', element.checked);
                                    break;
                                case 'placemark':
                                    // Смена категорий
                                    if($this.val() !== 'all') {
                                        if(global_bool_all_category_filter)
                                            changeCategoryAndFilter();
                                    } else {
                                        if (global_bool_not_all_category_filter) {
                                            global_bool_all_category_filter = false;
                                            changeAllCategoryAndFilter(element.checked)
                                        }
                                    }
                                    break;
                                case 'submark':
                                    // Смена фильтра
                                    if(global_bool_all_category_filter)
                                        changeCategoryAndFilter();
                                    break;
                            }
                        }
                    });

                    window.id_ymap
                        = window.zoom_ymap
                        = window.center_ymap
                        = window.custom_icons_ymap
                        = window.cluster_icon_ymap
                        = window.cluster_custom_icon_ymap
                        = window.cluster_size_ymap
                        = window.cluster_offset_ymap
                        = count
                        = tmp
                        = pk
                        = fields
                        = index
                        = elems
                        = key = null;

                    setTimeout(function () {
                        $('#id_ymap_panel_show_button').animate({
                            'left': '+=49'
                        }, 600);
                        $('.ymap_list_collection').css('z-index', '-1').eq(0).css('z-index', '0');
                        $('.ymap_link').eq(0).css('background', '#fff');
                        $('#id_filter_hint_link').on('click', function() {
                            $('#id_filter_hint_text').toggle(500);
                        });
                    }, 1000);

                } else {

                    alert('Err - load geoobjects')
                }
            }
        );
    });


    // Управление панелью ----------------------------------------------------------------------------------------------

    // Открыти и закрытие панели
    $(function () {
        $('#id_ymap_panel_show_button').on('click', function () {

            $(this).animate({
                'left': '-=49'
            }, 600);

            $('#id_ymap_panel').animate({
                'left': '+=340'
            }, 500);
        });

        $('#id_ymap_panel_close_button').on('click', function() {

            $('#id_ymap_panel').animate({
                'left': '-=340'
            }, 500);

            $('#id_ymap_panel_show_button').animate({
                'left': '+=49'
            }, 600);
        });
    });


    // Управление вкладками со списком коллекций
    $('#id_ymap_link_collection_placemark').on('click', function() {
        $('.ymap_list_collection').css('z-index', '-1');
        $('#id_ymap_list_collection_placemark').css('z-index', '0');
        $('.ymap_link').css('background', '#f8f8f8');
        $(this).css('background', '#fff');
    });

    $('#id_ymap_link_collection_polyline').on('click', function() {
        $('.ymap_list_collection').css('z-index', '-1');
        $('#id_ymap_list_collection_polyline').css('z-index', '0');
        $('.ymap_link').css('background', '#f8f8f8');
        $(this).css('background', '#fff');
    });

    $('#id_ymap_link_collection_polygon').on('click', function() {
        $('.ymap_list_collection').css('z-index', '-1');
        $('#id_ymap_list_collection_polygon').css('z-index', '0');
        $('.ymap_link').css('background', '#f8f8f8');
        $(this).css('background', '#fff');
    });

});
