/*
* Editor Yandex Maps.
* Creating thumbnails in the File Browser of CKEditor.
* The maximum image size is 966 pixels.
*
* Copyright (c) 2014 kebasyaty
* License MIT
*/

var runCKEditorResizeImage;

$( document ).ready( function() {
  'use strict';

  // Creating thumbnails and send image.
  function creatingThumbnails( fileUpload, formOfUpload ) {
    if ( fileUpload !== undefined ) {
      const fileType = fileUpload.type;

      /* Check the valid image type.
        (Проверяем допустимый тип изображения.) */
      if ( fileType !== 'image/jpeg' && fileType !== 'image/png' ) {
        formOfUpload.trigger( 'reset' );
        alert( window.gettext( 'Only JPG and PNG files.' ) );
        return;
      }

      /* Reduce image size to maximum.
        (Уменьшить размер изображения до максимального значения.) */
      const MAX_SIZE = 966;
      const MAX_WIDTH = MAX_SIZE;
      const MAX_HEIGHT = MAX_SIZE;
      const reader = new FileReader();
      const tempImg = new Image();
      let tempW;
      let tempH;
      const uploadIndicator = $( 'img.cke_image_upload_indicator' );

      uploadIndicator.css( 'display', 'block' );

      /* Listen to file download.
        (Слушаем загрузку файла.) */
      reader.onload = function( event ) { //
        /* Listen to file image.
          (Слушаем загрузку изображения.) */
        tempImg.onload = function() {
          tempW = tempImg.width;
          tempH = tempImg.height;

          /* Check the image size.
            (Проверить размер изображения.) */
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

          /* Optimize image size.
            (Оптимизировать размер изображения.) */
          const canvas = document.getElementById( 'cke_temp_canvas' );
          const ctx = canvas.getContext( '2d' );

          ctx.clearRect( 0, 0, canvas.width, canvas.height );
          canvas.width = tempW;
          canvas.height = tempH;
          ctx.drawImage( tempImg, 0, 0, tempW, tempH );

          const dataURI = canvas.toDataURL( fileType );

          const imageBlob = ( function() {
            const binary = atob( dataURI.split( ',' )[ 1 ] );
            const ab = new ArrayBuffer( binary.length );
            const ia = new Uint8Array( ab );

            for ( let idx = 0; idx < binary.length; idx++ ) {
              ia[ idx ] = binary.charCodeAt( idx );
            }
            return new Blob( [ ab ], { type: fileType } );
          } )();

          /* Send the image to the server.
            (Отправить изображение на сервер.) */
          const tempFormData = new FormData();
          tempFormData.append( 'upload', imageBlob, fileUpload.name );

          $.ajax( {
            type: 'POST',
            url: formOfUpload.attr( 'action' ),
            data: tempFormData,
            processData: false,
            contentType: false
          } ).fail( function() {
            window.console.log( window.gettext( 'Server Error ???' ) );
          } ).always( function() {
            uploadIndicator.css( 'display', 'none' );
            formOfUpload.trigger( 'reset' );
          } );
        };

        /* Add image for listening the event.
          (Добавить изображение для прослушивания события.) */
        tempImg.src = event.target.result;
      };

      /* Read in the image file as a data URL.
        (Добавить файл для прослушивания события.) */
      reader.readAsDataURL( fileUpload );
    }
  }

  /* Image size correction before adding to the CKEditor.
    (Коррекция размера изображения перед добавлением в CKEditor.) */
  try {
    if ( window.CKEDITOR !== undefined ) {
      window.CKEDITOR.on( 'dialogDefinition', function( event ) {
        const dialogName = event.data.name;
        const dialogDefinition = event.data.definition;
        const MAX_WIDTH = 322;

        if ( dialogName === 'image' ) {
          const onOk = dialogDefinition.onOk;

          dialogDefinition.onOk = function( event ) {
            const width = this.getContentElement( 'info', 'txtWidth' );
            const height = this.getContentElement( 'info', 'txtHeight' );
            const tmpWidth = +width.getValue();

            if ( tmpWidth > MAX_WIDTH ) {
              height.setValue( Math.floor( +height.getValue() * ( MAX_WIDTH / tmpWidth ) ) );
              width.setValue( MAX_WIDTH.toString() );
            }
            onOk && onOk.apply( this, event );
          };
        }
      } );
    }

    runCKEditorResizeImage = function() { //
      /* Listen to the click event on the `Upload` tab.
        (Прослушиваем событие `click` на вкладке `Загрузка`.) */
      $( document ).on( 'click', 'a.cke_dialog_tab_selected', function() {
        const $this = $( this );
        const commonParent = $this.parent().parent();
        const buttonLoadOnServer = commonParent.find( 'a.cke_dialog_ui_fileButton' );
        const parentOfButton = buttonLoadOnServer.parent();
        const iframeContents = commonParent.find( 'td.cke_dialog_ui_vbox_child iframe' ).contents();
        const formOfUpload = iframeContents.find( 'form' );
        let controlAgent = parentOfButton.find( 'div.cke_control_agent' );

        /* If there are no event listeners, create them.
          (Если нет прослушивателей событий, создаем их.) */
        if ( controlAgent.length > 0 ) {
          commonParent.find( 'tr.cke_info_upload_image' ).remove();
          controlAgent.off( 'click' );
          controlAgent.remove();
        }
        parentOfButton.css( 'position', 'relative' );

        $( '.cke_image_upload_indicator' ).remove();
        parentOfButton.parent().before( '<tr><td>' +
        '<img src="/static/djeym/img/loader.gif" class="cke_image_upload_indicator"' +
        ' style="display: none; margin: 20px 0;" alt="upload indicator"></td></tr>' );

        parentOfButton.parent().after( '<tr class="cke_info_upload_image"><td>' +
                  '<div>( ' + window.gettext( 'Image size will be optimized to 966 pixels.' ) +
                  ' )</div></td></tr>' );
        commonParent.find( 'tr.cke_info_upload_image div' ).css( {
          margin: '5px 0 10px',
          color: '#2196F3',
          'font-size': '14px',
          'font-weight': 'bold'
        } );

        parentOfButton.prepend( '<div class="cke_control_agent"></div>' );

        /* Control Agent - The layer for capturing events above the `Upload to the server` button
          (Control Agent - Слой для перехвата событий над кнопкой `Загрузить на сервер`.) */
        controlAgent = parentOfButton.find( 'div.cke_control_agent' );
        controlAgent.css( {
          position: 'absolute',
          top: '0',
          right: '0',
          bottom: '0',
          left: '0',
          'z-index': '1',
          cursor: 'pointer'
        } );

        controlAgent.on( 'click', function() { //
          /* Stop image processing for old browsers.
            (Останавливаем обработку изображения для устаревших браузеров.) */
          if ( !( window.File && window.FileReader && window.FileList && window.Blob ) ) {
            alert( window.gettext( 'The File APIs are not fully supported in this browser. ' +
                            'Upgrade your browser - http://browsehappy.com/' ) );
            return;
          }

          const fileUpload = formOfUpload.find( 'input[name="upload"]' )[ 0 ].files[ 0 ];
          creatingThumbnails( fileUpload, formOfUpload );
        } );
      } );
    };

    if ( !$( 'div' ).is( '#djeym-app' ) && !$( 'div' ).is( '#app' ) ) {
      runCKEditorResizeImage();
    }
  } catch ( err ) {
    window.console.log( err );
  }
} );
