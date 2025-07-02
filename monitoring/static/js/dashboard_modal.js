
  function showPurchaseOrderDetails(
    id, dateRecorded, po, customer, branch,
    dateReceived, targetDate, classification, description, serviceReportNumber,
    totalDays, manpowerTotal, manpowerStr, timeTotal, totalWorkHour,
    dateStarted, completionDate, cocNumber, drNumber, invoiceNumber, remarks, status
  ) {
    document.getElementById('po-id').innerText = id;
    document.getElementById('po-date-recorded').innerText = dateRecorded;
    document.getElementById('po-number').innerText = po;
    document.getElementById('po-customer').innerText = customer;
    document.getElementById('po-branch').innerText = branch;
    document.getElementById('po-date-received').innerText = dateReceived;
    document.getElementById('po-target-date').innerText = targetDate;
    document.getElementById('po-classification').innerText = classification;
    document.getElementById('po-description').innerText = description;
    document.getElementById('po-service-report-number').innerText = serviceReportNumber;
    document.getElementById('po-total-days').innerText = totalDays;
    document.getElementById('po-manpower-total').innerText = manpowerTotal;
    document.getElementById('po-manpower-string').innerText = manpowerStr;

    document.getElementById('po-time-total').innerText = timeTotal;
    document.getElementById('po-total-wh').innerText = totalWorkHour;
    document.getElementById('po-date-started').innerText = dateStarted;
    document.getElementById('po-completion-date').innerText = completionDate;
    document.getElementById('po-coc-number').innerText = cocNumber;
    document.getElementById('po-dr-number').innerText = drNumber;
    document.getElementById('po-invoice-number').innerText = invoiceNumber;
    document.getElementById('po-remarks').innerText = remarks;
    document.getElementById('po-status').innerText = status;

    

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('purchaseOrderModal'));
    modal.show();
  }
