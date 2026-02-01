function logDebug(value) {
  console.log(value);
}

function isElementInViewport(element) {
  try {
    const rect = element.getBoundingClientRect();
    return (
      rect.width > 0 &&
      rect.height > 0 &&
      rect.bottom >= 0 &&
      rect.right >= 0 &&
      rect.top <= window.innerHeight &&
      rect.left <= window.innerWidth
    );
  } catch {
    return false;
  }
}

function isTextLikeInput(element) {
  return (
    element instanceof HTMLInputElement &&
    /^(text|search|email|url|password)$/i.test(element.type)
  );
}

function isEditableElement(element) {
  if (!element) return false;

  if (
    element instanceof HTMLInputElement ||
    element instanceof HTMLTextAreaElement
  ) {
    if (element.disabled || element.readOnly) return false;
  }

  if (element instanceof HTMLElement && element.isContentEditable) {
    return isElementInViewport(element);
  }

  if (element instanceof HTMLTextAreaElement) {
    return isElementInViewport(element);
  }

  if (isTextLikeInput(element)) {
    return isElementInViewport(element);
  }

  return false;
}

function peekEditableText(element, maxLength = 6) {
  try {
    if (
      element instanceof HTMLInputElement ||
      element instanceof HTMLTextAreaElement
    ) {
      return element.value.slice(0, maxLength);
    }

    if (element.isContentEditable) {
      return element.innerText.slice(0, maxLength);
    }
  } catch {
    /* ignore */
  }

  return "";
}

function rankEditableElement(element) {
  const rect = element.getBoundingClientRect();
  let score = 0;

  if (element instanceof HTMLElement && element.isContentEditable) {
    score += 300;
  } else if (element instanceof HTMLTextAreaElement) {
    score += 200;
  } else {
    score += 100;
  }

  score += Math.min((rect.width * rect.height) / 500, 150);
  score += (window.innerHeight - rect.top) / 10;

  if (peekEditableText(element).length > 0) {
    score += 30;
  }

  if (element.tabIndex >= 0) {
    score += 10;
  }

  return score;
}

function describeEditableElement(element) {
  if (element.id) return "id=" + element.id;

  if (
    element instanceof HTMLInputElement ||
    element instanceof HTMLTextAreaElement
  ) {
    if (element.name) return "name=" + element.name;
  }

  if (element.className) return "class=" + element.className;

  const allEditables = Array.from(
    document.querySelectorAll('textarea, input, [contenteditable="true"]')
  );

  return "index=" + allEditables.indexOf(element);
}

function findBestEditableElement() {
  const focusedElement = document.activeElement;

  if (isEditableElement(focusedElement)) {
    return focusedElement;
  }

  let candidates;

  try {
    candidates = Array.from(
      document.querySelectorAll('textarea, input, [contenteditable="true"]')
    ).filter(isEditableElement);
  } catch {
    return null;
  }

  let best = null;
  let highestScore = -Infinity;

  for (const element of candidates) {
    try {
      const score = rankEditableElement(element);
      if (score > highestScore) {
        highestScore = score;
        best = element;
      }
    } catch {
      continue;
    }
  }

  return best;
}

function focusEditableElement(element) {
  if (!element) return;

  try {
    element.focus({ preventScroll: true });
  } catch {
    // ignore synthetic event failures
  }

  try {
    element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
    element.dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
    element.dispatchEvent(new MouseEvent("click", { bubbles: true }));
  } catch {
    // ignore synthetic event failures
  }

  try {
    element.dispatchEvent(new Event("focus", { bubbles: true }));
  } catch {
    // ignore synthetic event failures
  }
}

function findEditableByDescription(description) {
  const elements = Array.from(
    document.querySelectorAll('textarea, input, [contenteditable="true"]')
  );

  return (
    elements.find(
      (element) =>
        isEditableElement(element) &&
        describeEditableElement(element) === description
    ) || null
  );
}

function buildErrorResult(message) {
  return JSON.stringify({
    status: "error",
    message: message || "unknown error",
  });
}
