function entry(_unused) {
  let editableElement;

  try {
    editableElement = findBestEditableElement();
  } catch (error) {
    return buildErrorResult(extractErrorMessage(error));
  }

  if (!editableElement) {
    return buildErrorResult("no editable element found");
  }

  focusEditableElement(editableElement);

  try {
    return serializeEditableSelection(editableElement);
  } catch (error) {
    return buildErrorResult(extractErrorMessage(error));
  }
}

function isContentEditable(element) {
  return String(element.isContentEditable);
}

function serializeEditableSelection(element) {
  const pageUrl = safeParseCurrentUrl();

  return JSON.stringify({
    status: "ok",
    title: document.title,
    hostName: pageUrl.hostname,
    editableId: describeEditableElement(element),
    contentEditable: isContentEditable(element),
  });
}

function safeParseCurrentUrl() {
  try {
    return new URL(window.location.href);
  } catch (error) {
    throw new Error(extractErrorMessage(error));
  }
}

function extractErrorMessage(error) {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}

//# sourceURL=wenvi/browser/editable-select.js
