function entry(payload) {
  return setEditableText(payload);
}

function setEditableText(request) {
  let element = findBestEditableElement();
  if (!element) return buildErrorResult("no editable element found");

  if (element.tagName === "TEXTAREA" || element.tagName === "INPUT") {
    element.focus();
    element.value = request.text;
    element.dispatchEvent(new Event("input", { bubbles: true }));
  } else if (element.isContentEditable) {
    setContentEditableText(element, request.text);
  }
  return JSON.stringify({
    status: "ok",
  });
}
