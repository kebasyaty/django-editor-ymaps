$(document).ready(function() {

    // Color picker
    var $color = $('#id_color'),
        icon_name = $('.field-icon_name').find('p').text(),
        $stroke_color = $('#id_stroke_color'),
        $fill_color = $('#id_fill_color');

    // colorPicker - defaults colors
    $.fn.colorPicker.defaults.colors = [
        '82cdff', '1e98ff', '177bc9', '0e4779',
        '56db40', '1bad03', '97a100', '595959',
        'b3b3b3', 'f371d1', 'b51eff', '793d0e',
        'ffd21e', 'ff931e', 'e6761b', 'ed4543'
    ];

    if ($color !== undefined) $color.colorPicker({pickerDefault: $color.val()});
    if ($stroke_color !== undefined) $stroke_color.colorPicker({pickerDefault: $stroke_color.val()});
    if ($fill_color !== undefined) $fill_color.colorPicker({pickerDefault: $fill_color.val()});

    var $colorPicker_picker = $('div.colorPicker-picker');

    if (icon_name.length > 0 && (icon_name.search('Stretchy') > -1 || icon_name.search('#') == -1)) {
        $colorPicker_picker.hide();
    }

    $colorPicker_picker.css({'position': 'relative', 'top': '6px', 'left': '170px'});
});
