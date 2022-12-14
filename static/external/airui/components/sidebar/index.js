/////////////////////////////////////////////////////////////////////////////////////////
// "settings" module scripts

;(function($) {
  'use strict'
  $(function() {
    /////////////////////////////////////////////////////////////////////////////////////////
    // hide non top menu related settings
    if ($('.air__menuTop').length) {
      $('.hideIfMenuTop').css({
        pointerEvents: 'none',
        opacity: 0.4,
      })
    }

    /////////////////////////////////////////////////////////////////////////////////////////
    // toggle
    $('.air__sidebar__actionToggle').on('click', function() {
      $('body').toggleClass('air__sidebar--toggled')
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // custom scroll init

    if ($('.air__sidebar').length) {
      if (!/Mobi/.test(navigator.userAgent) && jQuery().perfectScrollbar) {
        $('.air__sidebar__scroll').perfectScrollbar({
          theme: 'airui',
        })
      }
    }

    /////////////////////////////////////////////////////////////////////////////////////////
    // switch

    $('.air__sidebar__switch input').on('change', function() {
      var el = $(this)
      var checked = el.is(':checked')
      var to = el.attr('to')
      var setting = el.attr('setting')
      if (checked) {
        $(to).addClass(setting)
      } else {
        $(to).removeClass(setting)
      }
    })

    $('.air__sidebar__switch input').each(function() {
      var el = $(this)
      var to = el.attr('to')
      var setting = el.attr('setting')
      if ($(to).hasClass(setting)) {
        el.attr('checked', true)
      }
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // colors

    $('.air__sidebar__select__item').on('click', function() {
      var el = $(this)
      var parent = el.parent()
      var to = parent.attr('to')
      var setting = el.attr('setting')
      var items = parent.find('> div')
      var classList = ''
      items.each(function() {
        var setting = $(this).attr('setting')
        if (setting) {
          classList = classList + ' ' + setting
        }
      })
      items.removeClass('air__sidebar__select__item--active')
      el.addClass('air__sidebar__select__item--active')
      $(to).removeClass(classList)
      $(to).addClass(setting)
    })

    $('.air__sidebar__select__item').each(function() {
      var el = $(this)
      var parent = el.parent()
      var to = parent.attr('to')
      var setting = el.attr('setting')
      var items = parent.find('> div')
      if ($(to).hasClass(setting)) {
        items.removeClass('air__sidebar__select__item--active')
        el.addClass('air__sidebar__select__item--active')
      }
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // type

    $('.air__sidebar__type__items input').on('change', function() {
      var el = $(this)
      var checked = el.is(':checked')
      var to = el.attr('to')
      var setting = el.attr('setting')
      $('body').removeClass('air__menu--compact air__menu--flyout air__menu--nomenu')
      if (checked) {
        $(to).addClass(setting)
      } else {
        $(to).removeClass(setting)
      }
    })

    $('.air__sidebar__type__items input').each(function() {
      var el = $(this)
      var to = el.attr('to')
      var setting = el.attr('setting')
      if ($(to).hasClass(setting)) {
        el.attr('checked', true)
      }
    })
  })
})(jQuery)
