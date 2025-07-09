  function handleModalClick(button) {
  showPurchaseOrderDetails(
    button.dataset.id,
    button.dataset.dateRecorded,
    button.dataset.po,
    button.dataset.customer,
    button.dataset.branch,
    button.dataset.dateReceived,
    button.dataset.targetDate,
    button.dataset.classification,
    button.dataset.description,
    button.dataset.serviceReportNumber,
    button.dataset.manpowerTotal,
    button.dataset.manpowerStr,
    button.dataset.manpowerType,
    button.dataset.totalDays,
    button.dataset.workingDaysTotal,
    button.dataset.workHoursTotal,
    button.dataset.dateStarted,
    button.dataset.completionDate,
    button.dataset.cocNumber,
    button.dataset.drNumber,
    button.dataset.invoiceNumber,
    button.dataset.remarks,
    button.dataset.status,
    button.dataset.targetDateDelayed
  );
}

  function showPurchaseOrderDetails(
  id, dateRecorded, po, customer, branch,
  dateReceived, targetDate, classification, description, serviceReportNumber,
  manpowerTotal, manpowerStr, manpowerType, totalDays, workingDaysTotal, workHoursTotal,
  dateStarted, completionDate, cocNumber, drNumber, invoiceNumber,
  remarks, status, targetDateDelayed
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
  document.getElementById('po-manpower-total').innerText = manpowerTotal;
  document.getElementById('po-manpower-string').innerText = manpowerStr;
  document.getElementById('po-manpower-type').innerText = manpowerType;
  document.getElementById('po-total-days').innerText = totalDays;
  document.getElementById('po-working-days-total').innerText = workingDaysTotal;
  document.getElementById('po-work-hours-total').innerText = workHoursTotal;
  document.getElementById('po-date-started').innerText = dateStarted;
  document.getElementById('po-completion-date').innerText = completionDate;
  document.getElementById('po-coc-number').innerText = cocNumber;
  document.getElementById('po-dr-number').innerText = drNumber;
  document.getElementById('po-invoice-number').innerText = invoiceNumber;
  document.getElementById('po-remarks').innerText = remarks;
  document.getElementById('po-status').innerText = status;

  const delayEl = document.getElementById('po-target-date-delayed');

  if (status === "Delayed" && targetDateDelayed) {
    delayEl.innerText = `(${targetDateDelayed} day${targetDateDelayed === '1' ? '' : 's'})`;
    delayEl.style.display = 'inline';
  } else {
    delayEl.innerText = "";
    delayEl.style.display = 'none';
  }

  const modal = new bootstrap.Modal(document.getElementById('purchaseOrderModal'));
  modal.show();
}

