(function () {
  var toggle = document.getElementById('adminPwToggle');
  var input = document.getElementById('id_password');
  if (toggle && input) {
    toggle.addEventListener('click', function () {
      var show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      toggle.querySelector('i').className = show ? 'fa fa-eye-slash' : 'fa fa-eye';
      toggle.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    });
  }
})();
