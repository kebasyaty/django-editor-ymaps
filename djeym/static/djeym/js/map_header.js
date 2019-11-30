var sliderValue = [5, 15, 25, 50, 80];
$(function () {
    $("#slider-range-max").slider({
        range: "max",
        min: 5,
        max: 80,
        value: 0,
        slide: function (event, ui) {
            if (sliderValue.indexOf(ui.value) === -1) return false;
            $("#slider-range-max #amount_location").val(ui.value)
            jQuery('#slider-range-max .ui-slider-handle').html('<span class="num">' + ui.value + ' км</span>')
            if (jQuery('#slider-range-max #amount_location').val() == 80) {
                jQuery('#slider-range-max .ui-slider-handle').html('<span class="num">50+ км</span>')
            } else {
            }

        }
    });
    $("#slider-range-max #amount_location").val($("#slider-range-max").slider("value"));
    jQuery('#slider-range-max .wraps .ui-slider-handle').html('<span class="num">5 км</span>')

});