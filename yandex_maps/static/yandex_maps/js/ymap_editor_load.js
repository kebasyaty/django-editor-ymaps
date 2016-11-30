ymaps.ready(function () {

    var Map,
        global_collections = {
            placemark: {},
            submark: {},
            polyline: {},
            polygon: {}
        },
        // дефолтный цвет для colorPicker
        global_default_color = '1e98ff',
        // context, tinymce
        global_target_textarea,
        global_tmp;


    // подключаем плагины-----------------------------------------------------------------------------------------------

    // TinyMCE
    $('#id_textarea_tinymce').tinymce({
        language: 'ru',
        theme: "advanced",
        plugins: "lists, paste, style, layer, table, advhr, advimage, advlink, emotions, insertdatetime, table," +
                   "searchreplace, contextmenu, directionality, inlinepopups, advlist, save, spellchecker, media",
        theme_advanced_buttons1: "insertfile, undo, redo, separator, bold, italic, separator, justifyleft, justifycenter, justifyright",
        theme_advanced_buttons1_add: "separator, formatselect, separator, fontsizeselect",
        theme_advanced_buttons2: "tablecontrols, separator, fontselect",
        theme_advanced_buttons3: "bullist, numlist, separator, outdent, indent, separator, forecolor, backcolor",
        theme_advanced_buttons3_add: "separator, charmap, separator, code, separator, image, separator, link, unlink, separator, save",

        extended_valid_elements: "hr[class|width|size|noshade], font[face|size|color|style], span[class|align|style]",
        theme_advanced_font_sizes: "0.375em,0.438em,0.500em,0.563em,0.625em,0.688em,0.750em,0.813em,0.875em,0.938em," +
                                   "1.000em,1.063em,1.125em,1.188em,1.250em,1.313em,1.375em,1.438em,1.500em," +
                                   "1.542em,1.583em,1.625em,1.667em,1.708em,1.750em",
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_resizing: false,
        theme_advanced_resizing_use_cookie: false,
        width: 427,
        height: 427,
        schema: 'html5',
        'content_css': '/static/yandex_maps/ymap_tinymce/css/admin_tinymce.css',
        theme_advanced_text_colors: '#ffffff,#000000,#82cdff,#1e98ff,#177bc9,#0e4779,' +
                                    '#56db40,#1bad03,#97a100,#595959,#b3b3b3,#f371d1,' +
                                    '#b51eff,#793d0e,#ffd21e,#ff931e,#e6761b,#ed4543',
        paste_use_dialog: false,
        paste_auto_cleanup_on_paste: true,
        paste_convert_headers_to_strong: false,
        paste_strip_class_attributes: true,
        paste_remove_styles_if_webkit: true,
        paste_remove_spans: true,
        paste_remove_styles: true,
        paste_retain_style_properties: "",

        paste_text_sticky: true,
        paste_text_sticky_default: true,

        file_browser_callback: djangoFileBrowser,

        onchange_callback: function () {
            tinymce.activeEditor.dom.addClass(tinymce.activeEditor.dom.select(
                '*, p, img, body, td, pre, h1, h2, h3, h4, h5, h6, a, span, table, hr, tr, th, ins, del, ' +
                'cite, acronym, abbr, li, ul, ol'
            ), 'ymap-tinymce');
        },

        save_onsavecallback: function () {
            global_target_textarea.val(tinymce.activeEditor.getContent().replace(/(src="(\.\.\/)+media)/, 'src="/media'));
            global_target_textarea = '';
            tinymce.activeEditor.setContent('');
            tinymce.activeEditor.undoManager.clear();
            $('#id_bat_tinymce').trigger('click');
            $('#id_popup_tinymce').hide(500);
        }
    });

    // colorPicker - defaults colors
    $.fn.colorPicker.defaults.colors = [
        '82cdff', '1e98ff', '177bc9', '0e4779',
        '56db40', '1bad03', '97a100', '595959',
        'b3b3b3', 'f371d1', 'b51eff', '793d0e',
        'ffd21e', 'ff931e', 'e6761b', 'ed4543'
    ];


    // СОЗДАЕМ КАРТУ----------------------------------------------------------------------------------------------------

    Map = new ymaps.Map('id_map_editor', {
        center: window.center_map,
        zoom: window.zoom_map
    },{hintCloseTimeout: null});


    // Добавляем события на карту---------------------------------------------------------------------------------------

    // открытие балуна - закрываем подсказки
    Map.events.add('balloonopen', function(){
        Map.hint.close();
    });

    // закрытие балуна - чистим элементы контента
    Map.balloon.events.add('beforeuserclose', function() {

        if ($('table').is('.table_balloon_context')) {

            var $table_balloon_context = $('.table_balloon_context');
            $table_balloon_context.find('*').off('click');
            $table_balloon_context.remove();
        }
    });

    // Меню действий
    Map.events.add('click', function(e){

        var coords = e.get('coords');

        Map.balloon.close();
        Map.balloon.open(coords, {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Выберите действие' +
                '</th></tr><tr valign=top><td style="padding-left:14px;">' +
                '<a href="javascript:void(0);" id="id_add_placemark">Добавить указатель</a><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_add_polyline">Добавить маршрут</a><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_add_polygon">Добавить территорию</a>' +
                '</td></tr>' +
                '</table>'
            }, {
                minHeight: 150,
                maxWidth: 200
            }
        );

        // Запуск функционала
        function runFunctional() {

            // Добавить маршрут
            $('#id_add_polyline').on('click', function () {
                Map.balloon.close();
                createPolyline(coords);
            });
            // Добавить указатель
            $('#id_add_placemark').on('click', function () {
                Map.balloon.close();
                createPlacemark(coords);
            });

            // Добавить территорию
            $('#id_add_polygon').on('click', function () {
                Map.balloon.close();
                createPolygon(coords);
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }
        waitLoadBalloon();
    });


    // ЛОМАНАЯ ЛИНИЯ ---------------------------------------------------------------------------------------------------

    // добавить новую линию
    function createPolyline(coords){

        var hintContent,
            balloonContent,
            pk = 0,
            strokeWidth,
            strokeColor,
            strokeOpacity,
            collectionID = 0,
            // dialog popup
            dialog = $('#id_dialog');

        // Выводим первичные настройки в балун
        Map.balloon.close();
        Map.balloon.open(coords, {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Добавить маршрут' +
                '</th></tr><tr valign=top><td>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_hint_text">Название маршрута</a><br>' +
                '<textarea id="id_hint_text"></textarea>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_balloon_text">Подробности</a><br>' +
                '<textarea id="id_balloon_text"></textarea>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_select_collection">Выбрать категорию</a><br>' +
                '<div class="gap"></div>' +
                '<label for="id_color_line">Цвет линии:</label><input id="id_color_line" type="text" value="">' +
                '</td><td>' +
                '<div class="gap"></div>' +
                '<label for="id_slider_width_line">Толщина линии:</label>' +
                '<div id="id_slider_width_line">' +
                '<div id="id_handle_width_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '<label for="id_slider_opacity_line">Прозрачность линии:</label>' +
                '<div id="id_slider_opacity_line">' +
                '<div id="id_handle_opacity_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="addPolyline">Добавить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="cancelPolyline">Отменить</a>' +
                '<div class="gap"></div>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                'После выбора "Добавить", кликните левой кнопкой мыши по карте и проложите маршрут.' +
                '</td></tr>' +
                '</table>'
            }, {
                minHeight: 290,
                maxWidth: 380
            }
        );

        // Запуск функционала
        function runFunctional() {

            // Подключение плагина для выбора цвета
            $('#id_color_line').colorPicker({pickerDefault: global_default_color});

            // Slider - толщина линии
            $( function() {
                var handle = $('#id_handle_width_line'),
                    tmp;

                $('#id_slider_width_line').slider({
                    min: 1,
                    max: 99,
                    value: 5,
                    create: function () {
                        tmp = $(this).slider('value');
                        handle.text(tmp);
                        strokeWidth = tmp;
                    },
                    slide: function (event, ui) {
                        tmp = ui.value;
                        handle.text(tmp);
                        strokeWidth = tmp;
                    }
                });
            });

            // Slider - прозрачность линии
            $( function() {
                var handle = $('#id_handle_opacity_line'),
                    tmp;

                $('#id_slider_opacity_line').slider({
                    min: 1,
                    max: 10,
                    value: 0.9  / 0.1,
                    create: function () {
                        tmp = ($(this).slider('value') * 0.1).toFixed(1);
                        handle.text(tmp);
                        strokeOpacity = tmp;
                    },
                    slide: function (event, ui) {
                        tmp = (ui.value  * 0.1).toFixed(1);
                        handle.text(tmp);
                        strokeOpacity = tmp;
                    }
                });
            });

            // открыть выбор коллекции
            $('#id_select_collection').on('click', function() {
                var $items_select_collection = $('#id_items_select_collection'),
                    checked;
                global_tmp = global_collections['polyline'];

                for (var key in global_tmp) {
                    key = parseInt(key);
                    checked = (key === collectionID) ? 'checked' : '';
                    $items_select_collection.append(
                        '<p><label for="id_radio-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="radio" id="id_radio-' + key + '" class="radio_collection"' +
                        ' name="collection" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                var radio_collection = $('.radio_collection');

                radio_collection.on('click', function () {
                    collectionID = parseInt($(this).val());
                    $('#id_collection_close_button').trigger('click');
                });

                radio_collection.checkboxradio();

                $('#id_popup_select_collection').show(500);
            });

            // закрыть выбор коллекции
            $('#id_collection_close_button').on('click', function() {
                $('#id_popup_select_collection').hide(500);
                $('#id_items_select_collection').text('');
            });

            // Добавить
            $('#addPolyline').on('click', function () {

                hintContent = $('#id_hint_text').val();
                balloonContent = $('#id_balloon_text').val();
                strokeColor = $('#id_color_line').val();

                if (hintContent.length === 0) {
                    dialog.text('Дайте название для маршрута.');
                    dialog.dialog('open');
                    return false;
                } else if (collectionID === 0) {
                    dialog.text('Выберите категорию.');
                    dialog.dialog('open');
                    return false;
                }

                var Polyline = new ymaps.Polyline([], {
                    hintContent: hintContent,
                    balloonContent: balloonContent,
                    pk: pk,
                    collectionType: 'collection_polyline',
                    collectionID: collectionID
                }, {
                    strokeWidth: strokeWidth,
                    strokeColor: strokeColor,
                    strokeOpacity: strokeOpacity
                });

                Polyline.events.add('contextmenu', function (e) {
                    contextMenuPolyline(e);
                });

                Map.geoObjects.add(Polyline);
                Polyline.editor.startEditing();
                Polyline.editor.startDrawing();

                Map.balloon.close();
            });

            // Отменить
            $('#cancelPolyline').on('click', function () {
                Map.balloon.close();
            });

            // добавить контекст в целевое текстовое поле - TinyMCE
            $('.link_textarea').on('click', function () {
                global_target_textarea = $($(this).data('id_name'));
                tinymce.activeEditor.setContent(global_target_textarea.val());
                $('#id_popup_tinymce').show(500);
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }

        waitLoadBalloon();
    }


    // контекстное меню для линий
    function contextMenuPolyline(e) {

        var obj = e.get('target'),
            // properties
            hintContent = obj.properties.get('hintContent'),
            balloonContent = obj.properties.get('balloonContentBody') || obj.properties.get('balloonContent') || '',
            pk = obj.properties.get('pk'),
            collectionID = obj.properties.get('collectionID'),
            // options
            strokeWidth = obj.options.get('strokeWidth'),
            strokeColor = obj.options.get('strokeColor'),
            strokeOpacity = parseFloat(obj.options.get('strokeOpacity')),
            // Coordinates
            Coordinates = obj.geometry.getCoordinates(),
            // dialog popup
            dialog = $('#id_dialog');

        // Выводим текущие настройки в балуне
        Map.balloon.close();
        Map.balloon.open([Coordinates[0][0], Coordinates[0][1]], {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Настройки маршрута' +
                '</th></tr><tr valign=top><td>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_hint_text">Название маршрута:</a><br>' +
                '<textarea id="id_hint_text">' + hintContent + '</textarea>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_balloon_text">Подробности:</a><br>' +
                '<textarea id="id_balloon_text">' + balloonContent + '</textarea>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_select_collection">Выбрать категорию</a><br>' +
                '<div class="gap"></div>' +
                '<label for="id_color_line">Цвет линии:&ensp;</label><input id="id_color_line" type="text" value="">' +
                '</td><td>' +
                '<div class="gap"></div>' +
                '<label for="id_slider_width_line">Толщина линии:</label>' +
                '<div id="id_slider_width_line">' +
                '<div id="id_handle_width_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '<label for="id_slider_opacity_line">Уровень прозрачности:</label>' +
                '<div id="id_slider_opacity_line">' +
                '<div id="id_handle_opacity_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="editPolyline">Редактировать</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="savePolyline">Сохранить</a>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="cancelPolyline">Отменить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="delPolyline">Удалить</a><br>' +
                '</td></tr>' +
                '</table>' +
                '<div id="id_bat_save"></div>' +
                '<div id="id_bat_tinymce"></div>'
            }, {
                minHeight: 270,
                maxWidth: 380
            }
        );

        // Запуск функционала
        function runFunctional() {

            var $id_color_line = $('#id_color_line');

            // Подключение плагина для выбора цвета
            $id_color_line.colorPicker({pickerDefault: strokeColor});

            // Временное применение цвета к линии, при редактировании
            $id_color_line.on('change', function () {
                obj.options.set('strokeColor', $(this).val());
            });

            // Slider - толщина линии
            $( function() {
                var handle = $('#id_handle_width_line'),
                    tmp;

                $('#id_slider_width_line').slider({
                    min: 1,
                    max: 99,
                    value: strokeWidth,
                    create: function () {
                        handle.text(strokeWidth);
                    },
                    slide: function (event, ui) {
                        tmp = ui.value;
                        handle.text(tmp);
                        strokeWidth = tmp;
                        obj.options.set('strokeWidth', tmp);
                    }
                });
            });

            // Slider - прозрачность линии
            $( function() {
                var handle = $('#id_handle_opacity_line'),
                    tmp;

                $('#id_slider_opacity_line').slider({
                    min: 1,
                    max: 10,
                    value: strokeOpacity / 0.1,
                    create: function () {
                        tmp = ($(this).slider('value') * 0.1).toFixed(1);
                        handle.text(tmp);
                    },
                    slide: function (event, ui) {
                        tmp = (parseFloat(ui.value)  * 0.1).toFixed(1);
                        handle.text(tmp);
                        strokeOpacity = tmp;
                        obj.options.set('strokeOpacity', tmp);
                    }
                });
            });
            
            // открыть выбор коллекции
            $('#id_select_collection').on('click', function() {
                var $items_select_collection = $('#id_items_select_collection'),
                    checked;
                global_tmp = global_collections['polyline'];

                for (var key in global_tmp) {
                    key = parseInt(key);
                    checked = (key === collectionID) ? 'checked' : '';
                    $items_select_collection.append(
                        '<p><label for="id_radio-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="radio" id="id_radio-' + key + '" class="radio_collection"' +
                        ' name="collection" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                var radio_collection = $('.radio_collection');

                radio_collection.on('click', function () {
                    collectionID = parseInt($(this).val());
                    $('#id_collection_close_button').trigger('click');
                });

                radio_collection.checkboxradio();

                $('#id_popup_select_collection').show(500);
            });

            // закрыть выбор коллекции
            $('#id_collection_close_button').on('click', function() {
                $('#id_popup_select_collection').hide(500);
                $('#id_items_select_collection').text('');
            });

            // Редактировать
            $('#editPolyline').on('click', function () {
                obj.editor.startEditing();
                obj.editor.startDrawing();
                Map.balloon.close();
            });

            // Сохранить
            $('#savePolyline').on('click', function () {

                hintContent = $('#id_hint_text').val();
                balloonContent = $('#id_balloon_text').val();
                strokeColor = $('#id_color_line').val();

                if (hintContent.length === 0) {
                    dialog.text('Дайте название для маршрута.');
                    dialog.dialog('open');
                    return false;
                } else if (collectionID === 0) {
                    dialog.text('Выберите категорию.');
                    dialog.dialog('open');
                    return false;
                }

                strokeOpacity = (strokeOpacity !== 1) ? strokeOpacity : '1.0';

                // Заполнить форму
                $('#id_hint_content').val(hintContent);
                $('#id_balloon_content').val(balloonContent);
                $('#id_stroke_width').val(strokeWidth);
                $('#id_stroke_color').val(strokeColor);
                $('#id_stroke_opacity').val(strokeOpacity);
                $('#id_coordinates').val($.toJSON(Coordinates));
                $('#id_pk').val(pk);
                $('#id_category').val(collectionID);
                $('#id_geo_type').val('polyline');
                $('#id_action').val('save');

                // отправляем форму
                $('#id_form_geoobjects').trigger('submit');
            });

            // действия после удачного сохранения или обновления
            $('#id_bat_save').on('click', function(){
                obj.getParent().remove(obj);
                Map.balloon.close();
            });

            // Отменить
            $('#cancelPolyline').on('click', function () {
                $('#id_pk').val(pk);
                $('#id_geo_type').val('polyline');
                $('#id_action').val('reload');

                obj.getParent().remove(obj);
                $('#id_form_geoobjects').trigger('submit');
                Map.balloon.close();
            });

            // Удалить
            $('#delPolyline').on('click', function () {

                if (pk > 0) {
                    $('#id_pk').val(pk);
                    $('#id_geo_type').val('polyline');
                    $('#id_action').val('delete');
                    $('#id_form_geoobjects').trigger('submit');
                }

                obj.getParent().remove(obj);
                Map.balloon.close();
            });

            // добавить контекст в целевое текстовое поле - TinyMCE
            $('.link_textarea').on('click', function () {
                global_target_textarea = $($(this).data('id_name'));
                tinymce.activeEditor.setContent(global_target_textarea.val());
                $('#id_popup_tinymce').show(500);
            });

            // обновление контента после редакции
            $('#id_bat_tinymce').on('click', function() {
                obj.properties.set('hintContent', $('#id_hint_text').val());
                obj.properties.set('balloonContent', $('#id_balloon_text').val());
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }

        waitLoadBalloon();
    }


    // МНОГОУГОЛЬНИК ---------------------------------------------------------------------------------------------------

    // добавить новый многоугольник
    function createPolygon(coords){

        var hintContent,
            balloonContent,
            strokeWidth,
            pk = 0,
            strokeColor,
            strokeOpacity,
            fillColor,
            fillOpacity,
            collectionID = 0,
            // dialog popup
            dialog = $('#id_dialog');

        // Выводим первичные настройки в балун
        Map.balloon.close();
        Map.balloon.open(coords, {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Добавить территорию' +
                '</th></tr><tr valign=top><td>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_hint_text">Название территории</a>' +
                '<textarea id="id_hint_text"></textarea><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_balloon_text">Подробности</a>' +
                '<textarea id="id_balloon_text"></textarea><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_select_collection">Выбрать категорию</a><br>' +
                '<div class="gap"></div>' +
                '<label for="id_color_line">Цвет линии:</label><input id="id_color_line" type="text" value="">' +
                '<div class="gap"></div>' +
                '<label for="id_color_line">Цвет заливки:</label><input id="id_color_fill" type="text" value="">' +
                '</td><td>' +
                '<div class="gap"></div>' +
                '<label for="id_slider_width_line">Толщина линии:</label>' +
                '<div id="id_slider_width_line">' +
                '<div id="id_handle_width_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '<label for="id_slider_opacity_line">Прозрачность линии:</label>' +
                '<div id="id_slider_opacity_line">' +
                '<div id="id_handle_opacity_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '<label for="id_slider_opacity_fill">Прозрачность заливки:</label>' +
                '<div id="id_slider_opacity_fill">' +
                '<div id="id_handle_opacity_fill" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="addPolygon">Добавить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="cancelPolygon">Отменить</a>' +
                '<div class="gap"></div>' +
                '</td></tr>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                'После выбора "Добавить", кликните левой кнопкой мыши по карте и обозначьте территорию.' +
                '</td></tr>' +
                '</table>'
            }, {
                minHeight: 340,
                maxWidth: 380
            }
        );

        // Запуск функционала
        function runFunctional() {

            // Подключение плагина для выбора цвета
            $('#id_color_line, #id_color_fill').colorPicker({pickerDefault: global_default_color});

            // Slider - толщина линии
            $( function() {
                var handle = $('#id_handle_width_line'),
                    tmp;

                $('#id_slider_width_line').slider({
                    min: 1,
                    max: 99,
                    value: 5,
                    create: function () {
                        tmp = $(this).slider('value');
                        handle.text(tmp);
                        strokeWidth = tmp;
                    },
                    slide: function (event, ui) {
                        tmp = ui.value;
                        handle.text(tmp);
                        strokeWidth = tmp;
                    }
                });
            });

            // Slider - прозрачность линии
            $( function() {
                var handle = $('#id_handle_opacity_line'),
                    tmp;

                $('#id_slider_opacity_line').slider({
                    min: 1,
                    max: 10,
                    value: 0.9  / 0.1,
                    create: function () {
                        tmp = ($(this).slider('value') * 0.1).toFixed(1);
                        handle.text(tmp);
                        strokeOpacity = tmp;
                    },
                    slide: function (event, ui) {
                        tmp = (ui.value  * 0.1).toFixed(1);
                        handle.text(tmp);
                        strokeOpacity = tmp;
                    }
                });
            });

            // Slider - прозрачность заливки
            $( function() {
                var handle = $('#id_handle_opacity_fill'),
                    tmp;

                $('#id_slider_opacity_fill').slider({
                    min: 1,
                    max: 10,
                    value: 0.9  / 0.1,
                    create: function () {
                        tmp = ($(this).slider('value') * 0.1).toFixed(1);
                        handle.text(tmp);
                        fillOpacity = tmp;
                    },
                    slide: function (event, ui) {
                        tmp = (ui.value  * 0.1).toFixed(1);
                        handle.text(tmp);
                        fillOpacity = tmp;
                    }
                });
            });

            // открыть выбор коллекции
            $('#id_select_collection').on('click', function() {
                var $items_select_collection = $('#id_items_select_collection'),
                    checked;
                global_tmp = global_collections['polygon'];

                for (var key in global_tmp) {
                    key = parseInt(key);
                    checked = (key === collectionID) ? 'checked' : '';
                    $items_select_collection.append(
                        '<p><label for="id_radio-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="radio" id="id_radio-' + key + '" class="radio_collection"' +
                        ' name="collection" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                var radio_collection = $('.radio_collection');

                radio_collection.on('click', function () {
                    collectionID = parseInt($(this).val());
                    $('#id_collection_close_button').trigger('click');
                });

                radio_collection.checkboxradio();

                $('#id_popup_select_collection').show(500);
            });

            // закрыть выбор коллекции
            $('#id_collection_close_button').on('click', function() {
                $('#id_popup_select_collection').hide(500);
                $('#id_items_select_collection').text('');
            });

            // Добавить
            $('#addPolygon').on('click', function () {

                hintContent = $('#id_hint_text').val();
                balloonContent = $('#id_balloon_text').val();
                strokeColor = $('#id_color_line').val();
                fillColor = $('#id_color_fill').val();

                if (hintContent.length === 0) {
                    dialog.text('Дайте название для территории.');
                    dialog.dialog('open');
                    return false;
                } else if (collectionID === 0) {
                    dialog.text('Выберите категорию.');
                    dialog.dialog('open');
                    return false;
                }

                var Polygon = new ymaps.Polygon([], {
                    hintContent: hintContent,
                    balloonContent: balloonContent,
                    pk: pk,
                    collectionID: collectionID,
                    collectionType: 'collection_polygon'
                }, {
                    strokeWidth: strokeWidth,
                    strokeColor: strokeColor,
                    strokeOpacity: strokeOpacity,
                    fillColor: fillColor,
                    fillOpacity: fillOpacity
                });

                Polygon.events.add('contextmenu', function (e) {
                    contextMenuPolygon(e);
                });

                Map.geoObjects.add(Polygon);
                Polygon.editor.startEditing();
                Polygon.editor.startDrawing();

                Map.balloon.close();
            });

            // Отменить
            $('#cancelPolygon').on('click', function () {
                Map.balloon.close();
            });

            // добавить контекст в целевое текстовое поле - TinyMCE
            $('.link_textarea').on('click', function () {
                global_target_textarea = $($(this).data('id_name'));
                tinymce.activeEditor.setContent(global_target_textarea.val());
                $('#id_popup_tinymce').show(500);
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }

        waitLoadBalloon();
    }

    // контекстное меню для полигонов
    function contextMenuPolygon(e) {

        var obj = e.get('target'),
            // properties
            hintContent = obj.properties.get('hintContent'),
            balloonContent = obj.properties.get('balloonContentBody') || obj.properties.get('balloonContent') || '',
            pk = obj.properties.get('pk'),
            collectionID = obj.properties.get('collectionID'),
            // options
            strokeWidth = obj.options.get('strokeWidth'),
            strokeColor = obj.options.get('strokeColor'),
            strokeOpacity = parseFloat(obj.options.get('strokeOpacity')),
            fillColor = obj.options.get('fillColor'),
            fillOpacity = parseFloat(obj.options.get('fillOpacity')),
            // Coordinates
            Coordinates = obj.geometry.getCoordinates(),
            // dialog popup
            dialog = $('#id_dialog');

        // Выводим текущие настройки в балун
        Map.balloon.close();
        Map.balloon.open(e.get('coords'), {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Настройки территории' +
                '</th></tr><tr valign=top><td>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_hint_text">Название маршрута:</a><br>' +
                '<textarea id="id_hint_text">' + hintContent + '</textarea>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_balloon_text">Подробности:</a><br>' +
                '<textarea id="id_balloon_text">' + balloonContent + '</textarea>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_select_collection">Выбрать категорию</a><br>' +
                '<div class="gap"></div>' +
                '<label for="id_color_line">Цвет линии:</label><input id="id_color_line" type="text" value="">' +
                '<div class="gap"></div>' +
                '<label for="id_color_line">Цвет заливки:</label><input id="id_color_fill" type="text" value="">' +
                '</td><td>' +
                '<div class="gap"></div>' +
                '<label for="id_slider_width_line">Толщина линии:</label>' +
                '<div id="id_slider_width_line">' +
                '<div id="id_handle_width_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '<label for="id_slider_opacity_line">Прозрачность линии:</label>' +
                '<div id="id_slider_opacity_line">' +
                '<div id="id_handle_opacity_line" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '<label for="id_slider_opacity_fill">Прозрачность заливки:</label>' +
                '<div id="id_slider_opacity_fill">' +
                '<div id="id_handle_opacity_fill" class="ui-slider-handle"></div>' +
                '</div><br>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="editPolygon">Редактировать</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="savePolygon">Сохранить</a>' +
                '</td></tr>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="cancelPolygon">Отменить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="delPolygon">Удалить</a>' +
                '</td></tr>' +
                '</table>' +
                '<div id="id_bat_save"></div>' +
                '<div id="id_bat_tinymce"></div>'
            }, {
                minHeight: 320,
                maxWidth: 380
            }
        );

        // Запуск функционала
        function runFunctional() {

            var $id_color_line = $('#id_color_line'),
                $id_color_fill = $('#id_color_fill');

            // Подключение плагина для выбора цвета
            $id_color_line.colorPicker({pickerDefault: strokeColor});
            $id_color_fill.colorPicker({pickerDefault: fillColor});

            // Временное применение цвета к линии, при редактировании
            $id_color_line.on('change', function () {
                obj.options.set('strokeColor', $(this).val());
            });

            // Временное применение цвета заливки к многоугольнику при редактировании
            $id_color_fill.on('change', function () {
                obj.options.set('fillColor', $(this).val());
            });

            // Slider - толщина линии
            $( function() {
                var handle = $('#id_handle_width_line'),
                    tmp;

                $('#id_slider_width_line').slider({
                    min: 1,
                    max: 99,
                    value: strokeWidth,
                    create: function () {
                        handle.text(strokeWidth);
                    },
                    slide: function (event, ui) {
                        tmp = ui.value;
                        handle.text(tmp);
                        strokeWidth = tmp;
                        obj.options.set('strokeWidth', tmp);
                    }
                });
            });

            // Slider - прозрачность линии
            $( function() {
                var handle = $('#id_handle_opacity_line'),
                    tmp;

                $('#id_slider_opacity_line').slider({
                    min: 1,
                    max: 10,
                    value: strokeOpacity  / 0.1,
                    create: function () {
                        tmp = ($(this).slider('value') * 0.1).toFixed(1);
                        handle.text(tmp);
                    },
                    slide: function (event, ui) {
                        tmp = (ui.value  * 0.1).toFixed(1);
                        handle.text(tmp);
                        strokeOpacity = tmp;
                        obj.options.set('strokeOpacity', tmp);
                    }
                });
            });

            // Slider - прозрачность заливки
            $( function() {
                var handle = $('#id_handle_opacity_fill'),
                    tmp;

                $('#id_slider_opacity_fill').slider({
                    min: 1,
                    max: 10,
                    value: fillOpacity  / 0.1,
                    create: function () {
                        tmp = ($(this).slider('value') * 0.1).toFixed(1);
                        handle.text(tmp);
                    },
                    slide: function (event, ui) {
                        tmp = (ui.value  * 0.1).toFixed(1);
                        handle.text(tmp);
                        fillOpacity = tmp;
                        obj.options.set('fillOpacity', tmp);
                    }
                });
            });

            // открыть выбор коллекции
            $('#id_select_collection').on('click', function() {
                var $items_select_collection = $('#id_items_select_collection'),
                    checked;
                global_tmp = global_collections['polygon'];

                for (var key in global_tmp) {
                    key = parseInt(key);
                    checked = (key === collectionID) ? 'checked' : '';
                    $items_select_collection.append(
                        '<p><label for="id_radio-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="radio" id="id_radio-' + key + '" class="radio_collection"' +
                        ' name="collection" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                var radio_collection = $('.radio_collection');

                radio_collection.on('click', function () {
                    collectionID = parseInt($(this).val());
                    $('#id_collection_close_button').trigger('click');
                });

                radio_collection.checkboxradio();

                $('#id_popup_select_collection').show(500);
            });

            // закрыть выбор коллекции
            $('#id_collection_close_button').on('click', function() {
                $('#id_popup_select_collection').hide(500);
                $('#id_items_select_collection').text('');
            });

            // Редактировать
            $('#editPolygon').click(function () {
                obj.editor.startEditing();
                obj.editor.startDrawing();
                Map.balloon.close();
            });

            // Сохранить
            $('#savePolygon').click(function () {

                hintContent = $('#id_hint_text').val();
                balloonContent = $('#id_balloon_text').val();
                strokeColor = $('#id_color_line').val();
                fillColor = $('#id_color_fill').val();

                if (hintContent.length === 0) {
                    dialog.text('Дайте название для территории.');
                    dialog.dialog('open');
                    return false;
                } else if (collectionID === 0) {
                    dialog.text('Выберите категорию.');
                    dialog.dialog('open');
                    return false;
                }

                strokeOpacity = (strokeOpacity !== 1) ? strokeOpacity : '1.0';
                fillOpacity = (fillOpacity !== 1) ? fillOpacity : '1.0';

                $('#id_hint_content').val(hintContent);
                $('#id_balloon_content').val(balloonContent);
                $('#id_stroke_width').val(strokeWidth);
                $('#id_stroke_color').val(strokeColor);
                $('#id_stroke_opacity').val(strokeOpacity);
                $('#id_fill_color').val(fillColor);
                $('#id_fill_opacity').val(fillOpacity);
                $('#id_coordinates').val($.toJSON(Coordinates));
                $('#id_pk').val(pk);
                $('#id_category').val(collectionID);
                $('#id_geo_type').val('polygon');
                $('#id_action').val('save');

                // отправляем форму
                $('#id_form_geoobjects').trigger('submit');
            });

            // действия после удачного сохранения или обновления
            $('#id_bat_save').on('click', function(){
                obj.getParent().remove(obj);
                Map.balloon.close();
            });

            // Отменить
            $('#cancelPolygon').click(function () {
                $('#id_pk').val(pk);
                $('#id_geo_type').val('polygon');
                $('#id_action').val('reload');

                obj.getParent().remove(obj);
                $('#id_form_geoobjects').trigger('submit');
                Map.balloon.close();
            });

            // Удалить
            $('#delPolygon').click(function () {
                if (pk > 0) {
                    $('#id_pk').val(pk);
                    $('#id_geo_type').val('polygon');
                    $('#id_action').val('delete');
                    $('#id_form_geoobjects').trigger('submit');
                }

                obj.getParent().remove(obj);
                Map.balloon.close();
            });

            // добавить контекст в целевое текстовое поле - TinyMCE
            $('.link_textarea').on('click', function () {
                global_target_textarea = $($(this).data('id_name'));
                tinymce.activeEditor.setContent(global_target_textarea.val());
                $('#id_popup_tinymce').show(500);
            });

            // обновление контента после редакции
            $('#id_bat_tinymce').on('click', function() {
                obj.properties.set('hintContent', $('#id_hint_text').val());
                obj.properties.set('balloonContent', $('#id_balloon_text').val());
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }

        waitLoadBalloon();
    }


    // УКАЗАТЕЛИ -------------------------------------------------------------------------------------------------------

    // добавить новый указатель
    function createPlacemark(coords) {

        var iconContent,
            hintContent,
            balloonContent,
            pk = 0,
            icon_name,
            iconColor,
            collectionID = 0,
            subCollectionIDs = [],
            // dialog popup
            dialog = $('#id_dialog');

        // Выводим первичные настройки в балун
        Map.balloon.close();
        Map.balloon.open(coords, {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Добавить указатель' +
                '</th></tr><tr valign=top><td>' +
                '<div class="gap"></div>' +
                '<input id="id_icon_text" type="text" value="" placeholder="Текст на иконке">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_hint_text">Название места</a>' +
                '<textarea id="id_hint_text"></textarea><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_balloon_text">Подробности</a>' +
                '<textarea id="id_balloon_text"></textarea><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_select_collection">Выбрать категорию</a><br>' +
                '<div class="gap"></div>' +
                '</td><td>' +
                '<div class="gap"></div>' +
                '<label for="id_icon">Иконка:&ensp;</label>' +
                '<img src="/static/yandex_maps/img/icons_map/blueStretchy.png" id="id_icon" data-icon_name="islands#blueStretchyIcon">' +
                '<div class="gap"></div>' +
                '<label for="id_color_icon">Цвет иконки:</label>' +
                '<input id="id_color_icon" type="text" value="">' +
                '<div id="id_fake_color_icon"></div>' +
                '<div class="gap"></div>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="addPlacemark">Добавить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="cancelPlacemark">Отменить</a>' +
                '<div class="gap"></div>' +
                '</td></tr>' +
                '</table>' +
                '<div id="id_bat_save"></div>'
            },
            {
                minHeight: 230,
                maxWidth: 380
            }
        );

        // Запуск функционала
        function runFunctional() {

            // placeholder
            $('input[placeholder]').placeholder();

            // Подключение плагина для выбора цвета
            $('#id_color_icon').colorPicker({pickerDefault: global_default_color});
            $('.colorPicker-picker').hide();
            $('#id_fake_color_icon').show();

            // открыть выбор коллекции
            $('#id_select_collection').on('click', function() {
                var $items_select_collection = $('#id_placemark_items_select_collection'),
                    checked,
                    $fieldset,
                    key;

                $fieldset = $items_select_collection.find('fieldset').eq(0);
                global_tmp = global_collections['placemark'];

                for (key in global_tmp) {
                    key = parseInt(key);
                    checked = (key === collectionID) ? 'checked' : '';
                    $fieldset.append(
                        '<p><label for="id_radio-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="radio" id="id_radio-' + key + '" class="radio_collection"' +
                        ' name="radio" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                $fieldset = $items_select_collection.find('fieldset').eq(1);
                global_tmp = global_collections['submark'];

                for (key in global_tmp) {
                    key = parseInt(key);
                    checked = ($.inArray(key, subCollectionIDs) > -1) ? 'checked' : '';
                    $fieldset.append(
                        '<p><label for="id_checkbox-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="checkbox" id="id_checkbox-' + key + '" class="checkbox_collection"' +
                        ' name="checkbox" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                var $radio_collection = $('.radio_collection'),
                    $checkbox_collection = $('.checkbox_collection');

                $radio_collection.on('click', function () {
                    collectionID = parseInt($(this).val());
                });

                $radio_collection.checkboxradio();

                $checkbox_collection.on('click', function() {
                    var $this = $(this),
                        sub_pk = parseInt($this.val()),
                        index_in_area = $.inArray(sub_pk, subCollectionIDs);

                    if (index_in_area > -1) {
                        subCollectionIDs.splice(index_in_area, 1);
                    } else {
                        subCollectionIDs.push(sub_pk);
                    }
                });

                $checkbox_collection.checkboxradio();

                $('#id_placemark_popup_select_collection').show(500);
            });

            // закрыть выбор коллекции
            $('#id_placemark_collection_close_button').on('click', function() {
                $('#id_placemark_popup_select_collection').hide(500);
                $('div#id_placemark_items_select_collection > fieldset').find('*:not(legend)').remove();
            });

            // Добавить
            $('#addPlacemark').on('click', function () {

                iconContent = $('#id_icon_text').val();
                hintContent = $('#id_hint_text').val();
                balloonContent = $('#id_balloon_text').val();
                icon_name = $('#id_icon').data('icon_name');
                iconColor = $('#id_color_icon').val();

                if (hintContent.length === 0) {
                    dialog.text('Дайте название для метки.');
                    dialog.dialog('open');
                    return false;
                } else if (collectionID === 0) {
                    dialog.text('Выберите категорию.');
                    dialog.dialog('open');
                    return false;
                } else if (subCollectionIDs.length === 0) {
                    dialog.text('Выберите подкатегорию.');
                    dialog.dialog('open');
                    return false;
                }

                $('#id_icon_content').val(iconContent);
                $('#id_icon_name').val(icon_name);
                $('#id_color').val(iconColor);
                $('#id_hint_content').val(hintContent);
                $('#id_balloon_content').val(balloonContent);
                $('#id_coordinates').val($.toJSON(coords));
                $('#id_pk').val(pk);
                $('#id_category').val(collectionID);
                $('#id_geo_type').val('placemark');

                var $subcategory = $('#id_subcategory');
                $subcategory.find('option').remove();
                for(var i = 0; i < subCollectionIDs.length; i++){
                    $subcategory.append('<option selected value="' + subCollectionIDs[i] + '"></option>');
                }

                $('#id_action').val('save');

                // отправляем форму
                $('#id_form_geoobjects').trigger('submit');
            });

            // действия после удачного сохранения или обновления
            $('#id_bat_save').on('click', function(){
                Map.balloon.close();
            });

            // Отменить
            $('#cancelPlacemark').on('click', function () {
                Map.balloon.close();
            });

            // добавить контекст в целевое текстовое поле - TinyMCE
            $('.link_textarea').on('click', function () {
                global_target_textarea = $($(this).data('id_name'));
                tinymce.activeEditor.setContent(global_target_textarea.val());
                $('#id_popup_tinymce').show(500);
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }

        waitLoadBalloon();
    }


    // контекстное меню для указателей
    function contextMenuPlacemark(e) {

        var obj = e.get('target'),
            // properties
            iconContent = obj.properties.get('iconContent') || '',
            hintContent = obj.properties.get('hintContent'),
            balloonContent = obj.properties.get('balloonContentBody') || '',
            pk = obj.properties.get('pk'),
            collectionID = obj.properties.get('collectionID'),
            subCollectionIDs =obj.properties.get('subCollectionIDs'),
            icon_name = obj.properties.get('IconName'),
            // options
            iconColor = obj.options.get('iconColor'),
            // Coordinates
            Coordinates = obj.geometry.getCoordinates(),
            // icon
            img_src = '',
            // dialog popup
            dialog = $('#id_dialog');

        $('.table_icons tr td').each(function() {
            if ($(this).data('icon_name') === icon_name) {
                img_src = $(this).data('img_src');
                return false;
            }
        });

        // Выводим первичные настройки в балун
        Map.balloon.close();
        Map.balloon.open(Coordinates, {
                contentBody: '<table class="table_balloon_context">' +
                '<tr><th colspan=2 align=center>' +
                'Настройки указателя' +
                '</th></tr><tr valign=top><td>' +
                '<div class="gap"></div>' +
                '<input id="id_icon_text" type="text" value="' + iconContent + '" placeholder="Текст на иконке">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_hint_text">Название места</a>' +
                '<textarea id="id_hint_text">' + hintContent + '</textarea><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" class="link_textarea" data-id_name="#id_balloon_text">Подробности</a>' +
                '<textarea id="id_balloon_text">' + balloonContent + '</textarea><br>' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="id_select_collection">Выбрать категорию</a><br>' +
                '<div class="gap"></div>' +
                '</td><td>' +
                '<div class="gap"></div>' +
                '<label for="id_icon">Иконка:&ensp;</label>' +
                '<img src="' + img_src + '" id="id_icon" data-icon_name="' + icon_name + '">' +
                '<div class="gap"></div>' +
                '<label for="id_color_icon">Цвет иконки:</label>' +
                '<input id="id_color_icon" type="text" value="">' +
                '<div id="id_fake_color_icon"></div>' +
                '<div class="gap"></div>' +
                '</td></tr><tr><td colspan=2 align=center class="balloon_footer">' +
                '<div class="gap"></div>' +
                '<a href="javascript:void(0);" id="savePlacemark">Сохранить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="cancelPlacemark">Отменить</a>&ensp;&ensp;' +
                '<a href="javascript:void(0);" id="delPlacemark">Удалить</a>' +
                '</td></tr>' +
                '</table>' +
                '<div id="id_bat_save"></div>' +
                '<div id="id_bat_tinymce"></div>'
            },
            {
                maxHeight: 230,
                minWidth: 360
            }
        );

        // Запуск функционала
        function runFunctional() {

            // placeholder
            $('input[placeholder]').placeholder();

            // Подключение плагина для выбора цвета
            $('.colorPicker-picker').remove();
            $('#id_color_icon').colorPicker({pickerDefault: iconColor});

            if (icon_name.search('Stretchy') == -1 && icon_name.search('#') > -1) {
                $('.colorPicker-picker').show();
                $('#id_fake_color_icon').hide();
            } else {
                $('#id_fake_color_icon').show();
                $('.colorPicker-picker').hide();
            }

            // открыть выбор коллекции
            $('#id_select_collection').on('click', function() {
                var $items_select_collection = $('#id_placemark_items_select_collection'),
                    checked,
                    $fieldset,
                    key;

                $fieldset = $items_select_collection.find('fieldset').eq(0);
                global_tmp = global_collections['placemark'];

                for (key in global_tmp) {
                    key = parseInt(key);
                    checked = (key === collectionID) ? 'checked' : '';
                    $fieldset.append(
                        '<p><label for="id_radio-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="radio" id="id_radio-' + key + '" class="radio_collection"' +
                        ' name="radio" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                $fieldset = $items_select_collection.find('fieldset').eq(1);
                global_tmp = global_collections['submark'];

                for (key in global_tmp) {
                    key = parseInt(key);
                    checked = ($.inArray(key, subCollectionIDs) > -1) ? 'checked' : '';
                    $fieldset.append(
                        '<p><label for="id_checkbox-' + key + '">' + global_tmp[key].properties.get('title') + '</label>' +
                        '<input type="checkbox" id="id_checkbox-' + key + '" class="checkbox_collection"' +
                        ' name="checkbox" ' + checked + ' value="' + key + '"></p>'
                    );
                }

                var $radio_collection = $('.radio_collection'),
                    $checkbox_collection = $('.checkbox_collection');

                $radio_collection.on('click', function () {
                    collectionID = parseInt($(this).val());
                });

                $radio_collection.checkboxradio();

                $checkbox_collection.on('click', function() {
                    var $this = $(this),
                        sub_pk = parseInt($this.val()),
                        index_in_area = $.inArray(sub_pk, subCollectionIDs);

                    if (index_in_area > -1) {
                        subCollectionIDs.splice(index_in_area, 1);
                    } else {
                        subCollectionIDs.push(sub_pk);
                    }
                });

                $checkbox_collection.checkboxradio();

                $('#id_placemark_popup_select_collection').show(500);
            });

            // закрыть выбор коллекции
            $('#id_placemark_collection_close_button').on('click', function() {
                $('#id_placemark_popup_select_collection').hide(500);
                $('div#id_placemark_items_select_collection > fieldset').find('*:not(legend)').remove();
            });

            // Добавить
            $('#savePlacemark').on('click', function () {

                iconContent = $('#id_icon_text').val();
                hintContent = $('#id_hint_text').val();
                balloonContent = $('#id_balloon_text').val();
                icon_name = $('#id_icon').data('icon_name');
                iconColor = $('#id_color_icon').val();

                if (hintContent.length === 0) {
                    dialog.text('Дайте название для метки.');
                    dialog.dialog('open');
                    return false;
                } else if (collectionID === 0) {
                    dialog.text('Выберите категорию.');
                    dialog.dialog('open');
                    return false;
                } else if (subCollectionIDs.length === 0) {
                    dialog.text('Выберите подкатегорию.');
                    dialog.dialog('open');
                    return false;
                }

                $('#id_icon_content').val(iconContent);
                $('#id_icon_name').val(icon_name);
                $('#id_color').val(iconColor);
                $('#id_hint_content').val(hintContent);
                $('#id_balloon_content').val(balloonContent);
                $('#id_coordinates').val($.toJSON(Coordinates));
                $('#id_pk').val(pk);
                $('#id_category').val(collectionID);
                $('#id_geo_type').val('placemark');

                var $subcategory = $('#id_subcategory');
                $subcategory.find('option').remove();
                for(var i = 0; i < subCollectionIDs.length; i++){
                    $subcategory.append('<option selected value="' + subCollectionIDs[i] + '"></option>');
                }

                $('#id_action').val('save');

                // отправляем форму
                $('#id_form_geoobjects').trigger('submit');
            });

            // действия после удачного сохранения или обновления
            $('#id_bat_save').on('click', function(){
                obj.getParent().remove(obj);
                Map.balloon.close();
            });

            // Отменить
            $('#cancelPlacemark').click(function () {
                $('#id_pk').val(pk);
                $('#id_geo_type').val('placemark');
                $('#id_action').val('reload');

                obj.getParent().remove(obj);
                $('#id_form_geoobjects').trigger('submit');
                Map.balloon.close();
            });

            // Удалить
            $('#delPlacemark').click(function () {
                if (pk > 0) {
                    $('#id_pk').val(pk);
                    $('#id_geo_type').val('placemark');
                    $('#id_action').val('delete');
                    $('#id_form_geoobjects').trigger('submit');
                }

                obj.getParent().remove(obj);
                Map.balloon.close();
            });

            // добавить контекст в целевое текстовое поле - TinyMCE
            $('.link_textarea').on('click', function () {
                global_target_textarea = $($(this).data('id_name'));
                tinymce.activeEditor.setContent(global_target_textarea.val());
                $('#id_popup_tinymce').show(500);
            });

            // обновление контента после редакции
            $('#id_bat_tinymce').on('click', function() {
                obj.properties.set('hintContent', $('#id_hint_text').val());
                obj.properties.set('balloonContent', $('#id_balloon_text').val());
            });
        }

        // Ждем загрузку балуна
        function waitLoadBalloon() {
            if (!$('table').is('.table_balloon_context')) {
                setTimeout(function () {
                    waitLoadBalloon();
                }, 100);
            } else {
                runFunctional();
                return false;
            }
        }

        waitLoadBalloon();
    }


    // Смена коллекций -------------------------------------------------------------------------------------------------

    // запуск смены коллекций
    function runChangeCollections() {

        // Смена коллекции маршрутов на карте
        $('#id_collection_polyline-menu').on('click', function () {

            var collection_id = $('select#id_collection_polyline > option:selected').val(),
                key;
            global_tmp = global_collections['polyline'];

            if (collection_id !== 'all-show' && collection_id !== 'all-hide') {

                collection_id = parseInt(collection_id);

                // Оставляем видимой выбранную коллекцию
                for (key in global_tmp) {
                    global_tmp[key].options.set('visible', false);
                }
                global_tmp[collection_id].options.set('visible', true);
            } else {
                for (key in global_collections['polyline']) {
                    global_tmp[key].options.set('visible', (collection_id === 'all-show'));
                }
            }
        });

        // Смена коллекции территорий на карте
        $('#id_collection_polygon-menu').on('click', function () {

            var collection_id = $('select#id_collection_polygon > option:selected').val(),
                key;
            global_tmp = global_collections['polygon'];

            if (collection_id !== 'all-show' && collection_id !== 'all-hide') {

                collection_id = parseInt(collection_id);

                // Оставляем видимой выбранную коллекцию
                for (key in global_tmp) {
                    global_tmp[key].options.set('visible', false);
                }
                global_tmp[collection_id].options.set('visible', true);
            } else {
                for (key in global_collections['polygon']) {
                    global_tmp[key].options.set('visible', (collection_id === 'all-show'));
                }
            }
        });

        // Смена коллекции меток на карте
        $('#id_collection_placemark-menu').on('click', function () {

            var collection_id = $('select#id_collection_placemark option:selected').val(),
                key;
            global_tmp = global_collections['placemark'];

            if (collection_id !== 'all-show' && collection_id !== 'all-hide') {

                collection_id = parseInt(collection_id);

                // Оставляем видимой выбранную коллекцию
                for (key in global_tmp) {
                    global_tmp[key].options.set('visible', false);
                }
                global_tmp[collection_id].options.set('visible', true);
            } else {
                for (key in global_collections['placemark']) {
                    global_tmp[key].options.set('visible', (collection_id === 'all-show'));
                }
            }
        });
        global_tmp = '';
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

            Polyline.events.add('contextmenu', function (e) {
                contextMenuPolyline(e);
            });

            // линию в коллекцию
            global_tmp[collection_id].add(Polyline);
        }
        global_tmp = '';
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

            Polygon.events.add('contextmenu', function (e) {
                contextMenuPolygon(e);
            });

            // полигон в коллекцию
            global_tmp[collection_id].add(Polygon);
        }
        global_tmp = '';
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

        global_tmp = global_collections['placemark'];

        for (var i = 0; i < count; i++) {

            tmp = placemarks[i];
            fields = tmp['fields'];
            collection_id = fields['category'];
            icon_name = fields['icon_name'];

            if (icon_name.search('#') > -1) {
                if (icon_name.search('Stretchy') == -1) {

                    Placemark = new ymaps.Placemark($.evalJSON(fields['coordinates']), {
                        hintContent: fields['hint_content'],
                        balloonContentHeader: fields['hint_content'],
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
                        balloonContentHeader: fields['hint_content'],
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

                custom_icon = window.custom_icons[icon_name];

                Placemark = new ymaps.Placemark($.evalJSON(fields['coordinates']), {
                    hintContent: fields['hint_content'],
                    balloonContentHeader: fields['hint_content'],
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

            Placemark.events.add('contextmenu', function (e) {
                contextMenuPlacemark(e);
            });

            // метку в коллекцию
            global_tmp[collection_id].add(Placemark);
        }
        global_tmp = '';
    }


    // AJAX-------------------------------------------------------------------------------------------------------------

    // Общая загрузка геообъектов
    $(function () {
        $.get(
            '/yandex_maps/load_geoobjects/',
            {id_map: window.id_map},
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
                        title;

                    // создать коллекции полилиний, полигонов и меток
                    for (var key in collections) {

                        collection = $.evalJSON(collections[key]);
                        count = collection.length;

                        $select_collection = $('#id_collection_' + key);

                        for (index = 0; index < count; index++) {
                            tmp = collection[index];
                            pk = tmp['pk'];
                            title = tmp['fields']['title'];
                            $select_collection.append('<option value="' + pk + '">' + title + '</option>');

                            Collection = new ymaps.GeoObjectCollection({properties: {title: title}});

                            if (key === 'placemark') Collection.options.set('draggable', true);

                            global_collections[key][pk] = Collection;
                            Map.geoObjects.add(Collection);
                        }
                    }

                    collections = collection = $select_collection = Collection = null;

                    geoobjects = data['geoobjects'];
                    data = null;

                    // добавить метки в коллекции
                    tmp = $.evalJSON(geoobjects['placemarks']);
                    geoobjects['placemarks'] = null;
                    if (tmp.length) {
                        addPlacemark(tmp);
                    }

                    // добавить полилинии в коллекци
                    tmp = $.evalJSON(geoobjects['polylines']);
                    geoobjects['polylines'] = null;
                    if (tmp.length) {
                        addPolyline(tmp);
                    }

                    // добавить полигоны в коллекции
                    tmp = $.evalJSON(geoobjects['polygons']);
                    geoobjects['polygons'] = null;
                    if (tmp.length) {
                        addPolygon(tmp);
                    }

                    // Запускается фильтр коллекций
                    $('select').selectmenu();
                    runChangeCollections();
                    setTimeout(function (){
                        $('#id_ymap_panel_show_button').animate({
                            'left': '+=49'
                        }, 800);
                    }, 1000);

                } else {

                    alert('Err - load geoobjects')
                }
            }
        );
    });

    // Сохранение и удаление геообъектов
    $('#id_form_geoobjects').on('submit', function(){

        var $form = $(this),
            dialog = $('#id_dialog');

        $.get(
            $form.attr('action'),
            $form.serialize(),
            function(data) {

                if (data['success']) {

                    $('#id_bat_save').trigger('click');

                    if (data['placemark'] !== undefined) {

                        addPlacemark($.evalJSON(data['placemark']));

                    } else if (data['polyline'] !== undefined) {

                        addPolyline($.evalJSON(data['polyline']));

                    } else if (data['polygon'] !== undefined) {

                        addPolygon($.evalJSON(data['polygon']));
                    }
                } else {
                    dialog.html(data['err_txt']);
                    dialog.dialog('open');
                }
            }
        );

        return false;
    });


    // Управление панелью ----------------------------------------------------------------------------------------------

    $(function () {
        $('#id_ymap_panel_show_button').on('click', function () {
            $(this).animate({
                'left': '-=49'
            }, 800);

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
            }, 800);
        });
    });

    // hide popup TinyMCE
    $('#id_tinymce_close_button').on('click', function() {
        global_target_textarea = '';
        tinymce.activeEditor.setContent('');
        tinymce.activeEditor.undoManager.clear();
        $('#id_popup_tinymce').hide(500);
    });

    // Run Dialog
    $('#id_dialog').dialog({
        autoOpen: false,
        show: {
            effect: 'blind',
            duration: 500
        },
        hide: {
            effect: 'explode',
            duration: 500
        }
    });


    // Загрузка иконок -------------------------------------------------------------------------------------------------
    $(function () {
        var $table_icons_tr_td,
            url_dir = '/static/yandex_maps/img/icons_map/',
            $table_icons = $('.table_icons'),
            all_icons = [],
            length_all_icons,
            tmp,
            standard_icons = [
                // standard icons - stretchy
                [url_dir + 'blueStretchy.png', 'islands#blueStretchyIcon'],
                [url_dir + 'redStretchy.png', 'islands#redStretchyIcon'],
                [url_dir + 'darkOrangeStretchy.png', 'islands#darkOrangeStretchyIcon'],
                [url_dir + 'nightStretchy.png', 'islands#nightStretchyIcon'],
                [url_dir + 'darkBlueStretchy.png', 'islands#darkBlueStretchyIcon'],
                [url_dir + 'pinkStretchy.png', 'islands#pinkStretchyIcon'],
                [url_dir + 'grayStretchy.png', 'islands#grayStretchyIcon'],
                [url_dir + 'brownStretchy.png', 'islands#brownStretchyIcon'],
                [url_dir + 'darkGreenStretchy.png', 'islands#darkGreenStretchyIcon'],
                [url_dir + 'violetStretchy.png', 'islands#violetStretchyIcon'],
                [url_dir + 'blackStretchy.png', 'islands#blackStretchyIcon'],
                [url_dir + 'yellowStretchy.png', 'islands#yellowStretchyIcon'],
                [url_dir + 'greenStretchy.png', 'islands#greenStretchyIcon'],
                [url_dir + 'orangeStretchy.png', 'islands#orangeStretchyIcon'],
                [url_dir + 'lightBlueStretchy.png', 'islands#lightBlueStretchyIcon'],
                [url_dir + 'oliveStretchy.png', 'islands#oliveStretchyIcon'],
                // standard icons - tag
                [url_dir + 'Home.png', 'islands#blueHomeIcon'],
                [url_dir + 'Airport.png', 'islands#blueAirportIcon'],
                [url_dir + 'Bar.png', 'islands#blueBarIcon'],
                [url_dir + 'Food.png', 'islands#blueFoodIcon'],
                [url_dir + 'Cinema.png', 'islands#blueCinemaIcon'],
                [url_dir + 'MassTransit.png', 'islands#blueMassTransitIcon'],
                [url_dir + 'Toilet.png', 'islands#blueToiletIcon'],
                [url_dir + 'Beach.png', 'islands#blueBeachIcon'],
                [url_dir + 'Zoo.png', 'islands#blueZooIcon'],
                [url_dir + 'Underpass.png', 'islands#blueUnderpassIcon'],
                [url_dir + 'Run.png', 'islands#blueRunIcon'],
                [url_dir + 'Bicycle.png', 'islands#blueBicycleIcon'],
                [url_dir + 'Garden.png', 'islands#blueGardenIcon'],
                [url_dir + 'Observation.png', 	'islands#blueObservationIcon'],
                [url_dir + 'EntertainmentCenter.png', 	'islands#blueEntertainmentCenterIcon'],
                [url_dir + 'Family.png', 'islands#blueFamilyIcon'],
                [url_dir + 'Theater.png', 'islands#blueTheaterIcon'],
                [url_dir + 'Book.png', 'islands#blueBookIcon'],
                [url_dir + 'Waterway.png', 	'islands#blueWaterwayIcon'],
                [url_dir + 'FuelStation.png', 'islands#blueFuelStationIcon'],
                [url_dir + 'RepairShop.png', 'islands#blueRepairShopIcon'],
                [url_dir + 'Post.png', 'islands#bluePostIcon'],
                [url_dir + 'WaterPark.png', 'islands#blueWaterParkIcon'],
                [url_dir + 'Worship.png', 'islands#blueWorshipIcon'],
                [url_dir + 'Fashion.png', 'islands#blueFashionIcon'],
                [url_dir + 'Waste.png', 'islands#blueWasteIcon'],
                [url_dir + 'Money.png', 'islands#blueMoneyIcon'],
                [url_dir + 'Hydro.png', 	'islands#blueHydroIcon'],
                [url_dir + 'Science.png', 	'islands#blueScienceIcon'],
                [url_dir + 'Auto.png', 	'islands#blueAutoIcon'],
                [url_dir + 'Shopping.png', 	'islands#blueShoppingIcon'],
                [url_dir + 'Sport.png', 	'islands#blueSportIcon'],
                [url_dir + 'Video.png', 	'islands#blueVideoIcon'],
                [url_dir + 'Railway.png', 	'islands#blueRailwayIcon'],
                [url_dir + 'Park.png', 		'islands#blueParkIcon'],
                [url_dir + 'Pocket.png', 	'islands#bluePocketIcon'],
                [url_dir + 'NightClub.png', 	'islands#blueNightClubIcon'],
                [url_dir + 'Pool.png', 	'islands#bluePoolIcon'],
                [url_dir + 'Medical.png', 		'islands#blueMedicalIcon'],
                [url_dir + 'Bicycle2.png', 	'islands#blueBicycle2Icon'],
                [url_dir + 'Vegetation.png', 	'islands#blueVegetationIcon'],
                [url_dir + 'Government.png', 	'islands#blueGovernmentIcon'],
                [url_dir + 'Circus.png', 	'islands#blueCircusIcon'],
                [url_dir + 'RapidTransit.png', 	'islands#blueRapidTransitIcon'],
                [url_dir + 'Education.png', 	'islands#blueEducationIcon'],
                [url_dir + 'Mountain.png', 	'islands#blueMountainIcon'],
                [url_dir + 'CarWash.png', 	'islands#blueCarWashIcon'],
                [url_dir + 'Factory.png', 	'islands#blueFactoryIcon'],
                [url_dir + 'Court.png', 		'islands#blueCourtIcon'],
                [url_dir + 'Hotel.png', 		'islands#blueHotelIcon'],
                [url_dir + 'Christian.png', 	'islands#blueChristianIcon'],
                [url_dir + 'Laundry.png', 	'islands#blueLaundryIcon'],
                [url_dir + 'Souvenirs.png', 	'islands#blueSouvenirsIcon'],
                [url_dir + 'Dog.png', 	'islands#blueDogIcon'],
                [url_dir + 'Leisure.png', 	'islands#blueLeisureIcon']
            ];

        for (var key in window.custom_icons) {
            all_icons.push([window.custom_icons[key][0], key]);
        }

        all_icons = all_icons.concat(standard_icons);
        length_all_icons = all_icons.length;

        for (var row = 0, count_rows = Math.ceil(length_all_icons / 4);
             row < count_rows; row++) {

            $table_icons.append('<tr><td></td><td></td><td></td><td></td></tr>');
        }

        $table_icons_tr_td = $('.table_icons tr td');

        $table_icons_tr_td.each(function(index, element) {

            if (index < length_all_icons) {

                tmp = all_icons[index][0];

                $(element).css(
                    {
                        'background': 'url("' + tmp + '") no-repeat center',
                        'background-size': 'contain'
                    }).data('icon_name', all_icons[index][1]).data('img_src', tmp);

            } else {

                return false;
            }
        });

        // выбор и смена иконки
        $table_icons_tr_td.on('click', function() {

            if ($('img').is('#id_icon')) {

                var $this = $(this),
                    $icon = $('#id_icon'),
                    icon_name = $this.data('icon_name');

                $icon.data('icon_name', icon_name);
                $icon.attr('src', $(this).data('img_src'));

                if (icon_name.search('Stretchy') == -1 && icon_name.search('#') > -1) {
                    $('#id_fake_color_icon').hide();
                    $('#id_color_icon').val('#1e98ff');
                    $('.colorPicker-picker').css('background-color', '#' + global_default_color).show();
                } else {
                    $('.colorPicker-picker').hide();
                    $('#id_fake_color_icon').show();
                }
            }
        });

        return false;
    });
});
