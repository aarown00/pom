  let isFormDirty = false;

  // Mark form as dirty when any field changes
  document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (form) {
      form.addEventListener("change", function () {
        isFormDirty = true;
      });

      form.addEventListener("submit", function () {
        isFormDirty = false; // Reset on successful save
      });

      window.addEventListener("beforeunload", function (e) {
        if (isFormDirty) {
          e.preventDefault(); // Some browsers require this
          e.returnValue = "You have unsaved changes. Are you sure you want to leave?";
          return "You have unsaved changes. Are you sure you want to leave?";
        }
      });
    }
  });

