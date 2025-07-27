
document.addEventListener('DOMContentLoaded', function () {
  const table = new DataTable('#poTable', {
    responsive: true,
    ordering: false,
    searching: false,
    paging: false,
    info: false,
    columnDefs: [
      { targets: 7, visible: false, searchable: false }
    ]
  });

  
});

