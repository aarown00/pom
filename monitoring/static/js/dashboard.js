
  document.addEventListener('DOMContentLoaded', function () {
  const table = new DataTable('#poTable', {
    responsive: true,
    ordering: false,
    searching: true,
    lengthMenu: [ [10, 20], [10, 20] ],


    columnDefs: [
      { targets: 7, visible: false, searchable: false } // hide ID column
    ],
    language: {
      search: 'Search P.O:', // leave empty so we can use our own label
      searchPlaceholder: 'Type P.O......' // <- placeholder
    },

    search: {
      return: true // allow full control over custom global search
    },
    initComplete: function () {
      const api = this.api();

      // Restrict global search to only the first column
      $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
        const searchValue = api.search().toLowerCase();
        const poNumber = data[0].toLowerCase(); // column 0 = PO number

        // If search is empty or PO matches, keep the row
        return searchValue === "" || poNumber.includes(searchValue);
      });

      // Redraw when the global search input changes
      document.querySelector('input[type="search"]').addEventListener('input', function () {
        const value = this.value;
        api.search(value).draw();
      });

      // Setup dropdown filters (same as before)
      api.columns().every(function () {
        const column = this;
        const index = column.index();
       if (index === 7 || index === 0 || index === 6) return; // skip index 0 and 7 and 1

        const headerCell = document.querySelector(
          `#poTable thead tr.filter-row th:nth-child(${index + 1})`
        );

        const select = document.createElement('select');
        select.innerHTML = `<option value="">ALL</option>`;
        headerCell.innerHTML = '';
        headerCell.appendChild(select);

        const uniqueValues = new Set();
        column.nodes().each(function (cell) {
          const value = cell.textContent.trim();
          if (value) uniqueValues.add(value);
        });

        [...uniqueValues].sort().forEach(function (value) {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          select.appendChild(option);
        });

        select.addEventListener('change', function () {
          const val = this.value;
          column.search(val !== '' ? `^${val}$` : '', true, false).draw();
        });
      });
    }
  });
});
