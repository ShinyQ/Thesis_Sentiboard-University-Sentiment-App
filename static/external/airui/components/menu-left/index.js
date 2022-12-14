/////////////////////////////////////////////////////////////////////////////////////////
// "menu-right" module scripts

;(function($) {
  'use strict'
  $(function() {
    /////////////////////////////////////////////////////////////////////////////////////////
    // toggle on resize

    ;(function() {
      var isTabletView = false
      function toggleMenu() {
        if (!isTabletView) {
          $('body').addClass('air__menu--toggled')
        }
      }
      if ($(window).innerWidth() <= 992) {
        toggleMenu()
        isTabletView = true
      }
      $(window).on('resize', function() {
        if ($(window).innerWidth() <= 992) {
          toggleMenu()
          isTabletView = true
        } else {
          isTabletView = false
        }
      })
    })()

    /////////////////////////////////////////////////////////////////////////////////////////
    // mobile toggle

    $('.air__menuLeft__mobileActionToggle').on('click', function() {
      $('body').toggleClass('air__menu--mobileToggled')
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // toggle

    $('.air__menuLeft__actionToggle').on('click', function() {
      $('body').toggleClass('air__menu--toggled')
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // menu logic

    $('.air__menuLeft__container').on(
      'click',
      '.air__menuLeft__submenu > .air__menuLeft__link',
      function() {
        var isMobile = window.innerWidth < 768
        if (
          ($('body').hasClass('air__menu--toggled') ||
            $('body').hasClass('air__menu--compact') ||
            $('body').hasClass('air__menu--flyout')) &&
          !isMobile
        ) {
          return
        }
        var submenu = $(this).closest('.air__menuLeft__submenu')
        var isActive = submenu.hasClass('air__menuLeft__submenu--active')
        $('.air__menuLeft__submenu--active').removeClass('air__menuLeft__submenu--active')
        if (!isActive) {
          submenu.addClass('air__menuLeft__submenu--active')
        }
        $('.air__menuLeft__submenu > .air__menuLeft__list')
          .stop()
          .slideUp(200)
        submenu
          .find('> .air__menuLeft__list')
          .stop()
          .slideToggle(200)
      },
    )

    /////////////////////////////////////////////////////////////////////////////////////////
    // flyout logic

    var flyoutTimers = {}

    $('.air__menuLeft__submenu').each(function() {
      $(this).attr(
        'flyout-id',
        Math.random()
          .toString(36)
          .substring(3),
      )
    })

    $('.air__menuLeft__container').on('mouseover', '.air__menuLeft__submenu', function() {
      var isActive = $('body').is('.air__menu--flyout, .air__menu--compact, .air__menu--toggled')
      var isUnfixed = $('body').is('.air__menu--unfixed')
      var id = $(this).attr('flyout-id')
      var isDesktop = window.innerWidth > 768
      var submenuList = $(this).find('> .air__menuLeft__list')
      var flyoutContainer = $('.air__menuFlyout[flyout-id=' + id + ']')
      clearInterval(flyoutTimers[id])
      if (isActive && isDesktop && submenuList.length && !flyoutContainer.length) {
        $('body').append('<div class="air__menuFlyout" flyout-id="' + id + '"></div>')
        var cloned = submenuList.clone()
        $('.air__menuFlyout[flyout-id=' + id + ']').html(cloned)
        var top = isUnfixed
          ? $(this).offset().top - $(window).scrollTop()
          : $(this).position().top + $('.air__menuLeft__container').position().top
        var left = $(this).offset().left + $(this).innerWidth()
        var itemHeight = $(this).innerHeight()
        var flyoutHeight = $('.air__menuFlyout[flyout-id=' + id + ']').innerHeight()
        $('.air__menuFlyout[flyout-id=' + id + ']')
          .css({
            top: top - flyoutHeight / 2 + itemHeight / 2,
            left: left - 10,
          })
          .addClass('air__menuFlyout--animation')
      }
    })

    $('.air__menuLeft__container').on('mouseout', '.air__menuLeft__submenu', function() {
      var isActive = $('body').is('.air__menu--flyout, .air__menu--compact, .air__menu--toggled')
      if (!isActive) {
        return
      }
      var id = $(this).attr('flyout-id')
      flyoutTimers[id] = setTimeout(function() {
        $('.air__menuFlyout[flyout-id=' + id + ']').remove()
      }, 100)
    })

    $('body').on('mouseover', '.air__menuFlyout', function() {
      var isActive = $('body').is('.air__menu--flyout, .air__menu--compact, .air__menu--toggled')
      if (!isActive) {
        return
      }
      var id = $(this).attr('flyout-id')
      clearInterval(flyoutTimers[id])
    })

    $('body').on('mouseout', '.air__menuFlyout', function() {
      var isActive = $('body').is('.air__menu--flyout, .air__menu--compact, .air__menu--toggled')
      if (!isActive) {
        return
      }
      var id = $(this).attr('flyout-id')
      flyoutTimers[id] = setTimeout(function() {
        $('.air__menuFlyout[flyout-id=' + id + ']').remove()
      }, 100)
    })

    /////////////////////////////////////////////////////////////////////////////////////////
    // set active menu item on load

    var url = window.location.href
    var page = url.substr(url.lastIndexOf('/') + 1)
    var currentItem = $('.air__menuLeft__container').find('a[href="' + page + '"]')
    currentItem.parent().toggleClass('air__menuLeft__item--active')
    currentItem
      .closest('.air__menuLeft__submenu')
      .addClass('air__menuLeft__submenu--active')
      .find('> .air__menuLeft__list')
      .show()
  })
})(jQuery)
