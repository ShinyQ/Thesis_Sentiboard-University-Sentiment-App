/////////////////////////////////////////////////////////////////////////////////////////
// "core" module scripts

;(function($) {
  'use strict'
  $(function() {
    /////////////////////////////////////////////////////////////////////////////////////////
    // custom scroll

    if ($('.air__customScroll').length) {
      if (!/Mobi/.test(navigator.userAgent) && jQuery().perfectScrollbar) {
        $('.air__customScroll').perfectScrollbar({
          theme: 'airui',
        })
      }
    }

    // tooltips & popovers
    $('[data-toggle=tooltip]').tooltip()
    $('[data-toggle=popover]').popover()
  })
})(jQuery)
