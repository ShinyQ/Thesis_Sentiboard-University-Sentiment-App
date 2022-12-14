$(document).ready(function() {
  $('.air__topbar__actionsDropdown .dropdown-menu').on('click', function() {
    $('.air__topbar__actionsDropdown').on('hide.bs.dropdown', function(event) {
      event.preventDefault() // stop hiding dropdown on click

      $('.air__topbar__actionsDropdown .nav-link').on('shown.bs.tab', function(e) {
        $('.air__topbar__actionsDropdown .dropdown-toggle').dropdown('update')
      })
    })
  })

  $(document, '.air__topbar__actionsDropdown .dropdown-toggle').mouseup(function(e) {
    var dropdown = $('.air__topbar__actionsDropdown')
    var dropdownMenu = $('.air__topbar__actionsDropdownMenu')

    if (
      !dropdownMenu.is(e.target) &&
      dropdownMenu.has(e.target).length === 0 &&
      dropdown.hasClass('show')
    ) {
      dropdown.removeClass('show')
      dropdownMenu.removeClass('show')
    }
  })

  $('.air__topbar__searchInput').on('focus', function() {
    $('.air__topbar__searchDropdown .dropdown-toggle').dropdown({
      offset: '5, 15',
    })
  })

  $('.air__topbar__searchInput').on('blur', function() {
    $('.air__topbar__searchDropdown .dropdown-toggle').dropdown('hide')
  })
})
