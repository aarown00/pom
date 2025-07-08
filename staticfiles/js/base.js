
  document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname.replace(/\/+$/, ''); // normalize: remove trailing slashes

    document.querySelectorAll('.sidebar .nav-link, .nav-tabs .nav-link').forEach(function (link) {
      const linkPath = link.getAttribute('href').replace(/\/+$/, '');

      // Exact match only
      if (linkPath === currentPath) {
        link.classList.add('active');
      }
    });
  });

