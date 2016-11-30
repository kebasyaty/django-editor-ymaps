$(document).ready(function() {

    // TinyMCE
    $('#id_hint_content, #id_balloon_content').tinymce({
        language: 'ru',
        theme: "advanced",
        plugins: "lists, paste, style, layer, table, advhr, advimage, advlink, emotions, insertdatetime, " +
                 "searchreplace, contextmenu, directionality, inlinepopups, advlist, spellchecker, media, save, table",
        theme_advanced_buttons1: "insertfile, undo, redo, separator, bold, italic, separator, justifyleft, justifycenter, justifyright",
        theme_advanced_buttons1_add: "separator, formatselect, separator, fontsizeselect",
        theme_advanced_buttons2: "tablecontrols, separator, fontselect",
        theme_advanced_buttons3: "bullist, numlist, separator, outdent, indent, separator, forecolor, backcolor",
        theme_advanced_buttons3_add: "separator, charmap, separator, code, separator, image, separator, link, unlink",

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
            tinymce.activeEditor.getContent().replace(/(src="(\.\.\/)+media)/, 'src="/media');
        }
    });

});
