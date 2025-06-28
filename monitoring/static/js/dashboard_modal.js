
  function showPurchaseOrderDetails(
    id, dateRecorded, po, customer, branch,
    dateEmail, targetDate, itemModel, description, serviceReport,
    totalDays, manpowerTotal, manpowerStr, timeTotal, totalWorkHour,
    dateStarted, completionDate, completionCode, deliveryCode, status
  ) {
    document.getElementById('po-id').innerText = id;
    document.getElementById('po-date-recorded').innerText = dateRecorded;
    document.getElementById('po-number').innerText = po;
    document.getElementById('po-customer').innerText = customer;
    document.getElementById('po-branch').innerText = branch;
    document.getElementById('po-date-email').innerText = dateEmail;
    document.getElementById('po-target-date').innerText = targetDate;
    document.getElementById('po-item-model').innerText = itemModel;
    document.getElementById('po-description').innerText = description;
    document.getElementById('po-service-report').innerText = serviceReport;
    document.getElementById('po-total-days').innerText = totalDays;
    document.getElementById('po-manpower-total').innerText = manpowerTotal;
    document.getElementById('po-manpower-string').innerText = manpowerStr;

    document.getElementById('po-time-total').innerText = timeTotal;
    document.getElementById('po-total-wh').innerText = totalWorkHour;
    document.getElementById('po-date-started').innerText = dateStarted;
    document.getElementById('po-completion-date').innerText = completionDate;
    document.getElementById('po-completion-code').innerText = completionCode;
    document.getElementById('po-delivery-code').innerText = deliveryCode;
    document.getElementById('po-status').innerText = status;

    

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('purchaseOrderModal'));
    modal.show();
  }
