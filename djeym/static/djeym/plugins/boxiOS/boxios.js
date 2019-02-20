/*
* boxiOS - jQuery plugin
*
* iOS Style for DOM elements - Radio, Checkboxes and Range.
*/

( function( $ ) {
  "use strict";

  // Checkbox
  $.fn.boxiosCheckbox = function( options ) {
    options = options || {};

    let $this,
      $label;

    return this.each( function( idx, elem ) {
      $this = $( elem );
      $label = $this.parent().parent();

      if ( options.hasOwnProperty( "size" ) ) {
        switch ( options.size ) {
          case "large":
            $label.css( "font-size", "18px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "31px" } );
            break;
          case "normal":
            $label.css( "font-size", "16px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "22px" } );
            break;
          case "middle":
            $label.css( "font-size", "14px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "25px" } );
            break;
          case "small":
            $label.css( "font-size", "12px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "22px" } );
            break;
        }
      } else {
        $label.find( ".boxios-ios-icon-display" )
          .css( { width: "22px" } );
      }

      if ( $this.prop( "checked" ) && options.hasOwnProperty( "jackColor" ) ) {
        $label.find( ".boxios-ios-checkbox__value" )
          .css( { backgroundColor: options.jackColor } );
      }

      $this.on( "change", function() {
        let $this = $( this );
        let $parent = $this.parent();

        if ( options.hasOwnProperty( "jackColor" ) ) {
          if ( $this.prop( "checked" ) ) {
            $parent.find( ".boxios-ios-checkbox__value" )
              .css( { backgroundColor: options.jackColor } );
          } else {
            $parent.find( ".boxios-ios-checkbox__value" ).removeAttr( "style" );
          }
        }
      } );
    } );
  };

  // Radio
  $.fn.boxiosRadio = function( options ) {
    options = options || {};

    let $this,
      $label;

    return this.each( function( idx, elem ) {
      $this = $( elem );
      $label = $this.parent().parent();

      if ( options.hasOwnProperty( "size" ) ) {
        switch ( options.size ) {
          case "large":
            $label.css( "font-size", "18px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "29px" } );
            break;
          case "normal":
            $label.css( "font-size", "16px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "26px" } );
            break;
          case "middle":
            $label.css( "font-size", "14px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "23px" } );
            break;
          case "small":
            $label.css( "font-size", "12px" );
            $label.find( ".boxios-ios-icon-display" )
              .css( { width: "20px" } );
            break;
        }
      } else {
        $label.find( ".boxios-ios-icon-display" )
          .css( { width: "26px" } );
      }

      if ( $this.prop( "checked" ) && options.hasOwnProperty( "jackColor" ) ) {
        $label.find( ".boxios-ios-radio__value" )
          .css( { backgroundColor: options.jackColor } );
      }

      $this.on( "change", function() {
        let $this = $( this );
        let $parent = $this.parent();

        $( "input[name=" + $this.attr( "name" ) + "]" ).parent()
          .find( ".boxios-ios-radio__value" ).removeAttr( "style" );

        if ( options.hasOwnProperty( "jackColor" ) ) {
          $parent.find( ".boxios-ios-radio__value" )
            .css( { backgroundColor: options.jackColor } );
        }
      } );
    } );
  };

  // Range
  $.fn.boxiosRange = function( options ) {
    options = options || {};

    let $this,
      $parent,
      targetElementValue;

    return this.each( function( idx, elem ) {
      $this = $( elem );
      $parent = $this.parent();
      targetElementValue = $this.data( "redirect_value_to" );

      if ( options.hasOwnProperty( "width" ) ) {
        $parent.css( "width", options.width );
      }
      if ( options.hasOwnProperty( "min" ) ) {
        $this.attr( "min", options.min );
      }
      if ( options.hasOwnProperty( "max" ) ) {
        $this.attr( "max", options.max );
      }
      if ( options.hasOwnProperty( "step" ) ) {
        $this.attr( "step", options.step );
      }
      if ( options.hasOwnProperty( "value" ) ) {
        $this.val( options.value );
      }

      if ( targetElementValue !== undefined ) {
        $( targetElementValue ).text( $this.val() );
      } else {
        $this.parent().find( ".boxios-ios-range-slider__value" ).text( $this.val() );
      }

      $this.on( "input", function() {
        let $this = $( this );
        let targetElementValue = $this.data( "redirect_value_to" );

        if ( targetElementValue !== undefined ) {
          $( targetElementValue ).text( $this.val() );
        } else {
          $this.parent().find( ".boxios-ios-range-slider__value" ).text( $this.val() );
        }
      } );
    } );
  };
} )( jQuery );
