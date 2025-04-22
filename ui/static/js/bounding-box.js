document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed.");

  const imageContainer = document.getElementById("image-container");
  const uploadedImage = document.getElementById("uploaded-image");

  if (!imageContainer || !uploadedImage) {
    console.error("Required DOM elements are missing.");
    return;
  }

  console.log("Image container and uploaded image found.");

  // Use the global detectionResult variable
  const detectionResult = window.detectionResult || {};
  console.log("Detection result:", detectionResult);

  const predictions = detectionResult.predictions || [];
  if (predictions.length === 0) {
    console.warn("No predictions found in detection result.");
    return;
  }

  // Create canvas element
  const canvas = document.createElement("canvas");
  canvas.style.position = "absolute";
  canvas.style.left = uploadedImage.offsetLeft + "px";
  canvas.style.top = uploadedImage.offsetTop + "px";
  canvas.style.pointerEvents = "none";
  canvas.style.zIndex = "10";

  const drawBoundingBoxes = () => {
    const ctx = canvas.getContext("2d");
    const containerWidth = uploadedImage.offsetWidth;
    const containerHeight = uploadedImage.offsetHeight;

    canvas.width = containerWidth;
    canvas.height = containerHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    predictions.forEach((pred) => {
      const widthScale = containerWidth / uploadedImage.naturalWidth;
      const heightScale = containerHeight / uploadedImage.naturalHeight;

      const boxLeft = (pred.x - pred.width / 2) * widthScale;
      const boxTop = (pred.y - pred.height / 2) * heightScale;
      const boxWidth = pred.width * widthScale;
      const boxHeight = pred.height * heightScale;

      ctx.strokeStyle = "red";
      ctx.lineWidth = 2;
      ctx.strokeRect(boxLeft, boxTop, boxWidth, boxHeight);
    });
  };

  imageContainer.style.position = "relative";
  imageContainer.appendChild(canvas);

  uploadedImage.onload = () => {
    drawBoundingBoxes();
    canvas.style.left = uploadedImage.offsetLeft + "px";
    canvas.style.top = uploadedImage.offsetTop + "px";
  };

  if (uploadedImage.complete) {
    drawBoundingBoxes();
    canvas.style.left = uploadedImage.offsetLeft + "px";
    canvas.style.top = uploadedImage.offsetTop + "px";
  }

  window.addEventListener("resize", () => {
    drawBoundingBoxes();
    canvas.style.left = uploadedImage.offsetLeft + "px";
    canvas.style.top = uploadedImage.offsetTop + "px";
  });
});
