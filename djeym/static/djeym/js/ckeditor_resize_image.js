/*
* Editor Yandex Maps.
* Creating thumbnails in the File Browser of CKEditor.
*
* Max size 966px.
* Максимальный размер изображения 966 пикселей.
*
* Copyright (c) 2014 genkosta
* License MIT
*/

var runCKEditorResizeImage;

$( document ).ready( function() {
  "use strict";

  try {
    CKEDITOR.on( "dialogDefinition", function( event ) {
      let dialogName = event.data.name;
      let dialogDefinition = event.data.definition;

      if ( dialogName === "image" ) {
        let onOk = dialogDefinition.onOk;

        dialogDefinition.onOk = function( event ) {
          let width = this.getContentElement( "info", "txtWidth" );
          let height = this.getContentElement( "info", "txtHeight" );
          let tmpWidth = +width.getValue();

          if ( tmpWidth > 322 ) {
            height.setValue( Math.floor( +height.getValue() * ( 322 / tmpWidth ) ) );
            width.setValue( "322" );
          }
          onOk && onOk.apply( this, event );
        };
      }
    } );

    runCKEditorResizeImage = function() { //
      // Listening to Tab "Upload".
      // (Прослушивание вкладки "Загрузка".)
      $( document ).on( "click", "a.cke_dialog_tab_selected", function( event ) {
        let $this = $( this );
        let commonParent = $this.parent().parent();
        let buttonLoadOnServer = commonParent.find( "a.cke_dialog_ui_fileButton" );
        let parentOfButton = buttonLoadOnServer.parent();
        let iframeContents = commonParent.find( "td.cke_dialog_ui_vbox_child iframe" ).contents();
        let formOfUpload = iframeContents.find( "form" );
        let controlAgent = parentOfButton.find( "div.cke_control_agent" );

        // If there are no event listeners, create them.
        // (Если нет прослушивателей событий, создайте их.)
        if ( controlAgent.length !== 0 ) {
          commonParent.find( "tr.cke_info_upload_image" ).remove();
          controlAgent.off( "click" );
          controlAgent.remove();
        }
        parentOfButton.css( "position", "relative" );

        parentOfButton.parent().before( "<tr class='cke_info_upload_image'><td>" +
                  "<img src='/static/djeym/img/loader.gif' class='cke_image_upload_indicator' " +
                  "style='display: none; margin: 20px 0;' alt='upload indicator'><div>" +
                  gettext( "Image size will be optimized to 966 pixels." ) + "</div></td></tr>" );
        commonParent.find( "tr.cke_info_upload_image td div" ).css( {
          margin: "20px 0 10px",
          color: "#0782c1",
          "font-size": "14px",
          "font-weight": "bold"
        } );

        parentOfButton.prepend( "<div class='cke_control_agent'></div>" );

        // Control Agent - The layer for capturing events above the "Upload to the server" button
        // (Control Agent - Слой для перехвата событий над кнопкой "Загрузить на сервер".)
        controlAgent = parentOfButton.find( "div.cke_control_agent" );
        controlAgent.css( {
          position: "absolute",
          top: "0",
          right: "0",
          bottom: "0",
          left: "0",
          "z-index": "1",
          cursor: "pointer"
        } );

        controlAgent.on( "click", function( event ) { //
          // Stop image processing for old browsers.
          // (Останавливаем обработку изображения для устаревших браузеров.)
          if ( !( window.File && window.FileReader && window.FileList && window.Blob ) ) {
            alert( gettext( "The File APIs are not fully supported in this browser. " +
                            "Upgrade your browser - http://browsehappy.com/" ) );
            return;
          }

          let fileUpload = formOfUpload.find( "input[name=\"upload\"]" )[ 0 ].files[ 0 ];

          creatingThumbnails( fileUpload, formOfUpload );
        } );
      } );

      // Creating thumbnails and send image.
      function creatingThumbnails( fileUpload, formOfUpload ) {
        if ( fileUpload !== undefined ) {
          let fileType = fileUpload.type;

          // Valid Image Type JPG and PNG.
          // (Допустимый тип изображения JPG и PNG.)
          if ( fileType !== "image/jpeg" && fileType !== "image/png" ) {
            formOfUpload.trigger( "reset" );
            alert( gettext( "Only JPG and PNG files." ) );
            return;
          }

          // Max size 966px.
          // (Максимальный размер изображения 966 пикселей.)
          const MAX_WIDTH = 966;

          const MAX_HEIGHT = 966;

          let reader = new FileReader();

          let tempImg = new Image();

          let tempW;

          let tempH;

          let uploadIndicator = $( "img.cke_image_upload_indicator" );

          uploadIndicator.css( "display", "block" );

          // Listen to file download.
          // (Слушаем загрузку файла.)
          reader.onload = function( event ) { //
            // Listen to file image.
            // Слушаем загрузку изображения.
            tempImg.onload = function() {
              tempW = tempImg.width;
              tempH = tempImg.height;

              // Check the image size.
              // (Проверить размер изображения.)
              if ( tempW > tempH ) {
                if ( tempW > MAX_WIDTH ) {
                  tempH = Math.floor( tempH * ( MAX_WIDTH / tempW ) );
                  tempW = MAX_WIDTH;
                }
              } else {
                if ( tempH > MAX_HEIGHT ) {
                  tempW = Math.floor( ( tempW * MAX_HEIGHT / tempH ) );
                  tempH = MAX_HEIGHT;
                }
              }

              // Optimize image size.
              // (Оптимизировать размер изображения.)
              let canvas = document.getElementById( "cke_temp_canvas" );

              let ctx = canvas.getContext( "2d" );

              ctx.clearRect( 0, 0, canvas.width, canvas.height );
              canvas.width = tempW;
              canvas.height = tempH;
              ctx.drawImage( tempImg, 0, 0, tempW, tempH );

              let dataURI = canvas.toDataURL( fileType );

              let imageBlob = ( function() {
                let binary = atob( dataURI.split( "," )[ 1 ] );

                let array = [];
                for ( let idx = 0; idx < binary.length; idx++ ) {
                  array.push( binary.charCodeAt( idx ) );
                }
                return new Blob( [ new Uint8Array( array ) ], { type: fileType } );
              } )();

              // Send the image to the server.
              // (Отправить изображение на сервер.)
              let tempFormData = new FormData();
              tempFormData.append( "upload", imageBlob, fileUpload.name );

              $.ajax( {
                type: "POST",
                url: formOfUpload.attr( "action" ),
                data: tempFormData,
                processData: false,
                contentType: false
              } ).done( function( response ) {

              // alert("Image uploaded successfully !!!\n( Изображение успешно загружено !!! )");
              } ).fail( function() {
                alert( gettext( "Server Error ???" ) );
              } ).always( function() {
                uploadIndicator.css( "display", "none" );
                formOfUpload.trigger( "reset" );
              } );
            };

            // Add image for listening the event.
            // (Добавить изображение для прослушивания события.)
            tempImg.src = event.target.result;
          };

          // Read in the image file as a data URL.
          // (Добавить файл для прослушивания события.)
          reader.readAsDataURL( fileUpload );
        }
      }
    };

    if ( !$( "form" ).is( "#id_form_geoobjects" ) ) {
      runCKEditorResizeImage();
    }
  } catch ( err ) {}
} );
