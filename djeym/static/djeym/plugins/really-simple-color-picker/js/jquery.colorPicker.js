/**
 * Really Simple Color Picker in jQuery
 *
 * Licensed under the MIT (MIT-LICENSE.txt) licenses.
 *
 * Copyright (c) 2008-2012
 * Lakshan Perera (www.laktek.com) & Daniel Lacy (daniellacy.com)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

( function( $ ) { //
  /**
    * Create a couple private variables.
  **/
  let selectorOwner;
  let activePalette;
  let cItterate = 0;
  let templates = {
    control: $( "<div class=\"colorPicker-picker\">&nbsp;</div>" ),
    palette: $( "<div id=\"colorPicker_palette\" class=\"colorPicker-palette\" />" ),
    swatch: $( "<div class=\"colorPicker-swatch\">&nbsp;</div>" ),
    hexLabel: $( "<label for=\"colorPicker_hex\">Hex: </label>" ),
    hexField: $( "<input type=\"text\" id=\"colorPicker_hex\" />" )
  };
  let transparent = "transparent";
  let lastColor;

  /**
    * Create our colorPicker function
  **/
  $.fn.colorPicker = function( options ) {
    return this.each( function() { //
      // Setup time. Clone new elements from our templates, set some IDs, make shortcuts, jazzercise.
      let element = $( this );
      let opts = $.extend( {}, $.fn.colorPicker.defaults, options );
      let defaultColor = $.fn.colorPicker.toHex(
        ( element.val().length > 0 ) ? element.val() : opts.pickerDefault
      );
      let newControl = templates.control.clone();
      let newPalette = templates.palette.clone().attr( "id", "colorPicker_palette-" + cItterate );
      let newHexLabel = templates.hexLabel.clone();
      let newHexField = templates.hexField.clone();
      let paletteId = newPalette[ 0 ].id;
      let swatch; let controlText;

      /**
        * Build a color palette.
      **/
      $.each( opts.colors, function( i ) {
        swatch = templates.swatch.clone();

        if ( opts.colors[ i ] === transparent ) {
          swatch.addClass( transparent ).text( "X" );
          $.fn.colorPicker.bindPalette( newHexField, swatch, transparent );
        } else {
          swatch.css( "background-color", "#" + this );
          $.fn.colorPicker.bindPalette( newHexField, swatch );
        }
        swatch.appendTo( newPalette );
      } );

      newHexLabel.attr( "for", "colorPicker_hex-" + cItterate );

      newHexField.attr( {
        id: "colorPicker_hex-" + cItterate,
        value: defaultColor
      } );

      newHexField.bind( "keydown", function( event ) {
        if ( event.keyCode === 13 ) {
          let hexColor = $.fn.colorPicker.toHex( $( this ).val() );
          $.fn.colorPicker.changeColor( hexColor || element.val() );
        }
        if ( event.keyCode === 27 ) {
          $.fn.colorPicker.hidePalette();
        }
      } );

      newHexField.on( "keyup", function( event ) {
        let hexColor = $.fn.colorPicker.toHex( $( event.target ).val() );
        $.fn.colorPicker.previewColor( hexColor || element.val() );
      } );

      $( "<div class=\"colorPicker_hexWrap\" />" ).append( newHexLabel ).appendTo( newPalette );

      newPalette.find( ".colorPicker_hexWrap" ).append( newHexField );
      if ( opts.showHexField === false ) {
        newHexField.hide();
        newHexLabel.hide();
      }

      $( "body" ).append( newPalette );

      newPalette.hide();

      /**
        * Build replacement interface for original color input.
      **/
      newControl.css( "background-color", defaultColor );

      newControl.on( "click", function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );

        if ( element.is( ":not(:disabled)" ) ) {
          $.fn.colorPicker.togglePalette( $( "#" + paletteId ), $( this ) );
        }
      } );

      if ( options && options.onColorChange ) {
        newControl.data( "onColorChange", options.onColorChange );
      } else {
        newControl.data( "onColorChange", function() {
        } );
      }

      controlText = element.data( "text" );

      if ( controlText ) { newControl.html( controlText ); }

      element.after( newControl );

      element.on( "change", function() {
        element.next( ".colorPicker-picker" ).css(
          "background-color", $.fn.colorPicker.toHex( $( this ).val() )
        );
      } );

      element.val( defaultColor );

      // Hide the original input.
      if ( element[ 0 ].tagName.toLowerCase() === "input" ) {
        try {
          element.attr( "type", "hidden" );
        } catch ( err ) { // oldIE doesn't allow changing of input.type
          element.css( "visibility", "hidden" ).css( "position", "absolute" );
        }
      } else {
        element.hide();
      }

      cItterate++;
    } );
  };

  /**
    * Extend colorPicker with... all our functionality.
  **/
  $.extend( true, $.fn.colorPicker, {

    /**
        * Return a Hex color, convert an RGB value and return Hex, or return false.
        *
        * Inspired by http://code.google.com/p/jquery-color-utils
    **/
    toHex: function( color ) { //
      // If we have a standard or shorthand Hex color, return that value.
      if ( color.match( /[0-9A-F]{6}|[0-9A-F]{3}$/i ) ) {
        return ( color.charAt( 0 ) === "#" ) ? color : ( "#" + color );

        // Alternatively, check for RGB color, then convert and return it as Hex.
      } else if ( color.match( /^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/ ) ) {
        let c = ( [ parseInt( RegExp.$1, 10 ), parseInt( RegExp.$2, 10 ),
          parseInt( RegExp.$3, 10 ) ] );
        let pad = function( str ) {
          if ( str.length < 2 ) {
            for ( let i = 0, len = 2 - str.length; i < len; i++ ) {
              str = "0" + str;
            }
          }

          return str;
        };

        if ( c.length === 3 ) {
          let r = pad( c[ 0 ].toString( 16 ) );
          let g = pad( c[ 1 ].toString( 16 ) );
          let b = pad( c[ 2 ].toString( 16 ) );

          return "#" + r + g + b;
        }

        // Otherwise we wont do anything.
      } else {
        return false;
      }
    },

    /**
        * Check whether user clicked on the selector or owner.
    **/
    checkMouse: function( event, paletteId ) {
      let selector = activePalette;
      let selectorParent = $( event.target ).parents( "#" + selector.attr( "id" ) ).length;

      if ( event.target === $( selector )[ 0 ] ||
        event.target === selectorOwner[ 0 ] || selectorParent > 0 ) {
        return;
      }

      $.fn.colorPicker.hidePalette();
    },

    /**
        * Hide the color palette modal.
    **/
    hidePalette: function() {
      $( document ).off( "mousedown", $.fn.colorPicker.checkMouse );

      $( ".colorPicker-palette" ).hide();
    },

    /**
        * Show the color palette modal.
    **/
    showPalette: function( palette ) {
      let hexColor = selectorOwner.prev( "input" ).val();

      palette.css( {
        top: selectorOwner.offset().top + ( selectorOwner.outerHeight() ),
        left: selectorOwner.offset().left
      } );

      $( "#color_value" ).val( hexColor );

      palette.show();

      $( document ).on( "mousedown", $.fn.colorPicker.checkMouse );
    },

    /**
        * Toggle visibility of the colorPicker palette.
    **/
    togglePalette: function( palette, origin ) { //
      // selectorOwner is the clicked .colorPicker-picker.
      if ( origin ) {
        selectorOwner = origin;
      }

      activePalette = palette;

      if ( activePalette.is( ":visible" ) ) {
        $.fn.colorPicker.hidePalette();
      } else {
        $.fn.colorPicker.showPalette( palette );
      }
    },

    /**
        * Update the input with a newly selected color.
    **/
    changeColor: function( value ) {
      selectorOwner.css( "background-color", value );
      selectorOwner.prev( "input" ).val( value ).change();

      $.fn.colorPicker.hidePalette();

      selectorOwner.data( "onColorChange" ).call( selectorOwner,
        $( selectorOwner ).prev( "input" ).attr( "id" ), value );
    },

    /**
        * Preview the input with a newly selected color.
    **/
    previewColor: function( value ) {
      selectorOwner.css( "background-color", value );
    },

    /**
        * Bind events to the color palette swatches.
    */
    bindPalette: function( paletteInput, element, color ) {
      color = color || $.fn.colorPicker.toHex( element.css( "background-color" ) );

      element.on( "click", function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );

        lastColor = color;
        $.fn.colorPicker.changeColor( color );
      } ).on( "mouseover", function() {
        lastColor = paletteInput.val();
        paletteInput.val( color );
        $.fn.colorPicker.previewColor( color );
      } ).on( "mouseout", function() {
        paletteInput.val( selectorOwner.css( "background-color" ) );
        paletteInput.val( lastColor );
        $.fn.colorPicker.previewColor( lastColor );
      } );
    }
  } );

  /**
    * Default colorPicker options.
    *
    * These are publibly available for global modification using a setting such as:
    *
    * $.fn.colorPicker.defaults.colors = ["151337", "111111"]
    *
    * They can also be applied on a per-bound element basis like so:
    *
    * $("#element1").colorPicker({pickerDefault: "efefef", transparency: true});
    * $("#element2").colorPicker({pickerDefault: "333333", colors: ["333333", "111111"]});
    *
  **/
  $.fn.colorPicker.defaults = {

    // colorPicker default selected color.
    pickerDefault: "ffffff",

    // Default color set.
    colors: [ "#1abc9c", "#16a085", "#2ecc71", "#27ae60", "#3498db", "#2980b9",
      "#9b59b6", "#8e44ad", "#34495e", "#2c3e50", "#f1c40f", "#f39c12",
      "#e67e22", "#d35400", "#e74c3c", "#c0392b", "#ecf0f1", "#bdc3c7",
      "#95a5a6", "#7f8c8d" ],

    // If we want to simply add more colors to the default set, use addColors.
    addColors: [],

    // Show hex field
    showHexField: true
  };
} )( jQuery );
