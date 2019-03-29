/*
* Admin panel - Plug-in initialization "colorPicker"
* (Панель администратора - Инициализация плагина "colorPicker")
* Copyright (c) 2014 genkosta
* License MIT
*/

$( document ).ready( function() {
  "use strict";

  // Color picker
  let $categoryColor = $( "#id_category_color" );
  let $strokeColor = $( "#id_stroke_color" );
  let $fillColor = $( "#id_fill_color" );
  let $colorPickerPicker;
  let defaultsYMapsColors = [
    "82cdff", "1e98ff", "177bc9", "0e4779",
    "56db40", "1bad03", "97a100", "595959",
    "b3b3b3", "f371d1", "b51eff", "793d0e",
    "ffcc00", "ff931e", "e6761b", "ed4543"
  ];

  $.fn.colorPicker.defaults.colors = [
    "FFFFFF", "F08080", "CD5C5C", "FF0000", "FF1493", "C71585",
    "800080", "F0E68C", "BDB76B", "6A5ACD", "483D8B", "3CB371",
    "2E8B57", "9ACD32", "008000", "808000", "20B2AA", "008B8B",
    "00BFFF", "CD853F", "A52A2A", "708090", "34495e", "999966",
    "333333", "FFCC66"
  ].concat( defaultsYMapsColors );

  if ( $categoryColor !== undefined ) {
    $categoryColor.colorPicker(
      { pickerDefault: $categoryColor.val() } );
  }
  if ( $strokeColor !== undefined ) {
    $strokeColor.colorPicker(
      { pickerDefault: $strokeColor.val() } );
  }
  if ( $fillColor !== undefined ) {
    $fillColor.colorPicker(
      { pickerDefault: $fillColor.val() } );
  }

  $colorPickerPicker = $( ".colorPicker-picker" );
  $colorPickerPicker.css( { position: "relative", top: "3px", left: "170px" } );
} );
