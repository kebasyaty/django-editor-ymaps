# -*- coding: utf-8 -*-

# Presets default
raw_presets = [
    {
        "position": 1,
        "title": "Text",
        "icon": "mdi-note-text-outline",
        "html": '<p>\r\n<div style="color:#e91e63;">{}</div>\r\n<div style="color:#3f51b5;">( Add your text to the address - YANDEX MAPS / Maps / Map / Presets > Text | Html )</div>\r\n</p>'.format('Добавьте свой текст по адресу - ЯНДЕКС КАРТЫ / Карты / Карта /Пресеты / Text | Html'),
        "js": "",
        "description": '<div style="color:#3F51B5;">{}.</div>\r\n<div style="color:#E91E63;">( Inserts text information - Link, advertisement, etc. )</div>'.format('Вставляет текстовую информацию - Ссылка, реклама и т.д.'),
        "slug": "text"
    },
    {
        "position": 2,
        "title": "Likes",
        "icon": "mdi-thumb-up-outline",
        "html": "<table style=\"width:100%;min-width:240px;\">\r\n    <tr>\r\n        <td style=\"width:32px;\">\r\n            <span id=\"id_djeym_hand_like\" class=\"mdi mdi-thumb-up mdi-24px\" data-obj_type=\"djeymObjectType\" data-obj_pk=\"djeymObjectID\" style=\"color:#FFC107;cursor:pointer;\"></span>\r\n        </td>\r\n        <td style=\"width:32px;\">\r\n            <span id=\"id_djeym_hand_dislike\" class=\"mdi mdi-thumb-down mdi-24px\" data-obj_type=\"djeymObjectType\" data-obj_pk=\"djeymObjectID\" style=\"color:#424242;cursor:pointer;\"></span>\r\n        </td>\r\n        <td style=\"padding: 0 0 10px 10px;\">\r\n            <div style=\"position:relative;height:16px;font-size:14px;\">\r\n                <span id=\"id_djeym_count_like\" style=\"position:absolute;top:0;left:0;color:#424242;\">0</span>\r\n                <span id=\"id_djeym_count_dislike\" style=\"position:absolute;top:0;right:0;color:#424242;\">0</span>\r\n            </div>\r\n            <div style=\"height:8px;background:#424242;\">\r\n                <div id=\"id_djeym_progress_likes\" style=\"width:50%;height:8px;background:#FFC107;\"></div>\r\n            </div>\r\n        </td>\r\n    </tr>\r\n</table>\r\n<div class=\"djeymUpdateInfoPreset\" onclick=\"window.djeymUpdateLikes( 'djeymObjectType', djeymObjectID );\"></div>",
        "js": "var djeymUpdateLikes = function( djeymObjectType, djeymObjectID ) {\r\n  $.get( \"/djeym/ajax-update-likes/\", {\r\n    djeymObjectType: djeymObjectType,\r\n    djeymObjectID: djeymObjectID\r\n  } )\r\n    .done( function( data ) {\r\n      let like = +data.like;\r\n      let dislike = +data.dislike;\r\n      let progress = Math.round( ( like / ( like + dislike ) ) * 100 );\r\n      if ( progress > 100 ) { progress = 100; }\r\n      $( \"#id_djeym_count_like\" ).text( like );\r\n      $( \"#id_djeym_count_dislike\" ).text( dislike );\r\n      $( \"#id_djeym_progress_likes\" ).css( \"width\", progress.toString() + \"%\" );\r\n    } )\r\n    .fail( function( jqxhr, textStatus, error ) {\r\n      let err = textStatus + \", \" + error;\r\n      console.log( \"Request Failed: \" + err );\r\n    } );\r\n};\r\n$( document ).on( \"click\", \"#id_djeym_hand_like, #id_djeym_hand_dislike\", function() {\r\n  let $this = $( this );\r\n  $.post( \"/djeym/ajax-update-likes/\", {\r\n    djeymObjectType: $this.data( \"obj_type\" ),\r\n    djeymObjectID: $this.data( \"obj_pk\" ),\r\n    targetAction: $this.attr( \"id\" ),\r\n    csrfmiddlewaretoken: window.djeymCSRFToken\r\n  } )\r\n    .done( function( data ) {\r\n      let like = +data.like;\r\n      let dislike = +data.dislike;\r\n      let progress = Math.round( ( like / ( like + dislike ) ) * 100 );\r\n      if ( progress > 100 ) { progress = 100; }\r\n      $( \"#id_djeym_count_like\" ).text( like );\r\n      $( \"#id_djeym_count_dislike\" ).text( dislike );\r\n      $( \"#id_djeym_progress_likes\" ).css( \"width\", progress.toString() + \"%\" );\r\n    } )\r\n    .fail( function( jqxhr, textStatus, error ) {\r\n      let err = textStatus + \", \" + error;\r\n      console.log( \"Request Failed: \" + err );\r\n    } );\r\n} );",
        "description": '<div style="color:#3F51B5;">{0}\r\n{1}</div>\r\n<div style="color:#E91E63;">( Accepts likes on geo-objects.  It works only in one selected place - Header, Description or Footer.)</div>'.format('Принимает лайки на гео-объектах.', 'Работает только в одном выбранном месте - Заголовок, Описание или Подвал.'),
        "slug": "likes"
    }
]
