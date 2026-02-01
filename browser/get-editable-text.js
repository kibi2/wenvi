function entry(_unused) {
  return getEditableText();
}

function getEditableText() {
  let element = findBestEditableElement();
  let text = "";
  if (!element) return "";
  if (
    element instanceof HTMLTextAreaElement ||
    element instanceof HTMLInputElement
  ) {
    text = element.value ?? "";
  }
  if (element.isContentEditable) {
    text = normalizeProseMirrorText(element.textContent ?? "");
  }
  return JSON.stringify({
    status: "ok",
    text: text,
  });
}
