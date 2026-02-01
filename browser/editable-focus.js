function entry(payload) {
  return focusRequestedEditable(payload);
}

function focusRequestedEditable(request) {
  let editableElement;

  try {
    editableElement = findEditableByDescription(request.editableId);
  } catch (error) {
    return buildErrorResult(extractErrorMessage(error));
  }

  if (!editableElement) {
    return buildErrorResult("no editable element found");
  }

  focusEditableElement(editableElement);
  return buildOkResult();
}

function buildOkResult() {
  return JSON.stringify({ status: "ok" });
}

function extractErrorMessage(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}

//# sourceURL=wenvi/browser/editable-focus.js
