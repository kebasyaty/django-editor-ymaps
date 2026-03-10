"use strict";

// Check the DOM is loaded
const _domReady = (callBack) => {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", callBack);
  } else {
    callBack();
  }
};

export { _domReady as domReady };
