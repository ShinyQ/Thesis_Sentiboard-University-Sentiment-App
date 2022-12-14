/////////////////////////////////////////////////////////////////////////////////////////
// "menu-right" module scripts

;(function($) {
  'use strict'
  $(function() {
    /////////////////////////////////////////////////////////////////////////////////////////
    // mobile toggle

    $('.air__menuTop__mobileActionToggle').on('click', function() {
      $('body').toggleClass('air__menu--mobileToggled')
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // menu logic

    $('.air__menuTop__container').on(
      'click',
      '.air__menuTop__submenu > .air__menuTop__link',
      function() {
        var isMobile = window.innerWidth < 768
        if (!isMobile) {
          return
        }
        var submenu = $(this).closest('.air__menuTop__submenu')
        var isActive = submenu.hasClass('air__menuTop__submenu--active')
        $('.air__menuTop__submenu--active').removeClass('air__menuTop__submenu--active')
        if (!isActive) {
          submenu.addClass('air__menuTop__submenu--active')
        }
        $('.air__menuTop__submenu > .air__menuTop__list')
          .stop()
          .slideUp(200)
        submenu
          .find('> .air__menuTop__list')
          .stop()
          .slideToggle(200)
      },
    )

    /////////////////////////////////////////////////////////////////////////////////////////
    // flyout logic

    var flyoutTimers = {}

    $('.air__menuTop__submenu').each(function() {
      $(this).attr(
        'flyout-id',
        Math.random()
          .toString(36)
          .substring(3),
      )
    })

    $('.air__menuTop__container').on('mouseover', '.air__menuTop__submenu', function() {
      var id = $(this).attr('flyout-id')
      var isDesktop = window.innerWidth > 768
      var submenuList = $(this).find('> .air__menuTop__list')
      var flyoutContainer = $('.air__menuFlyout[flyout-id=' + id + ']')
      clearInterval(flyoutTimers[id])
      if (isDesktop && submenuList.length && !flyoutContainer.length) {
        $('body').append('<div class="air__menuFlyout" flyout-id="' + id + '"></div>')
        var cloned = submenuList.clone()
        $('.air__menuFlyout[flyout-id=' + id + ']').html(cloned)
        var top = $(this).offset().top + $(this).innerHeight()
        var left = $(this).offset().left
        var itemWidth = $(this).innerWidth()
        var flyoutWidth = $('.air__menuFlyout[flyout-id=' + id + ']').innerWidth()
        $('.air__menuFlyout[flyout-id=' + id + ']')
          .css({
            top: top - 3,
            left: left - flyoutWidth / 2 + itemWidth / 2,
          })
          .addClass('air__menuFlyout--animation')
      }
    })

    $('.air__menuTop__container').on('mouseout', '.air__menuTop__submenu', function() {
      var id = $(this).attr('flyout-id')
      flyoutTimers[id] = setTimeout(function() {
        $('.air__menuFlyout[flyout-id=' + id + ']').remove()
      }, 100)
    })

    $('body').on('mouseover', '.air__menuFlyout', function() {
      var id = $(this).attr('flyout-id')
      clearInterval(flyoutTimers[id])
    })

    $('body').on('mouseout', '.air__menuFlyout', function() {
      var id = $(this).attr('flyout-id')
      flyoutTimers[id] = setTimeout(function() {
        $('.air__menuFlyout[flyout-id=' + id + ']').remove()
      }, 100)
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // set active menu item on load

    var url = window.location.href
    var page = url.substr(url.lastIndexOf('/') + 1)
    var currentItem = $('.air__menuTop__container').find('a[href="' + page + '"]')
    currentItem.parent().toggleClass('air__menuTop__item--active')
    currentItem
      .closest('.air__menuTop__submenu')
      .addClass('air__menuTop__submenu--active')
      .find('> .air__menuTop__list')
      .show()
  })
})(jQuery)
