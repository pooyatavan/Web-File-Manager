document.addEventListener('DOMContentLoaded', function() {
    var lightbox = document.getElementById("lightbox");
    var lightboxImg = document.getElementById("lightbox-img");
    var captionText = document.getElementById("caption");
    var currentImageIndex = 0;
    var images = document.querySelectorAll('.gallery-item-image');
    var scale = 1; // Initialize scale for zoom
    var originX = 50, originY = 50; // Initialize transform origin

    // Function to show the selected image
    function showImage(index) {
        if (index >= images.length) {
            currentImageIndex = 0;
        } else if (index < 0) {
            currentImageIndex = images.length - 1;
        } else {
            currentImageIndex = index;
        }

        lightboxImg.src = images[currentImageIndex].dataset.image;
        captionText.innerHTML = images[currentImageIndex].alt;
        lightbox.style.display = "flex";
        scale = 1; // Reset zoom when image changes
        lightboxImg.style.transform = "scale(1)";
        lightboxImg.style.transformOrigin = '50% 50%'; // Reset origin
    }

    // Event listener for each image to open the lightbox
    images.forEach((item, index) => {
        item.addEventListener('click', function() {
            showImage(index);
        });
    });

    // Close the lightbox
    var span = document.getElementsByClassName("close")[0];
    span.onclick = function() {
        lightbox.style.display = "none";
        lightboxImg.style.transform = "scale(1)";
        scale = 1; // Reset scale when closed
    };

    // Zoom in and out using the scroll wheel at the cursor position
    lightboxImg.addEventListener('wheel', function(event) {
        event.preventDefault(); // Prevent page scrolling

        // Get the mouse position relative to the image
        var rect = lightboxImg.getBoundingClientRect();
        var offsetX = event.clientX - rect.left; // Mouse X position over the image
        var offsetY = event.clientY - rect.top;  // Mouse Y position over the image
        var originX = (offsetX / rect.width) * 100; // Convert to percentage
        var originY = (offsetY / rect.height) * 100; // Convert to percentage

        lightboxImg.style.transformOrigin = `${originX}% ${originY}%`; // Set origin for zoom

        if (event.deltaY < 0) {
            // Zoom in
            scale += 0.1;
        } else {
            // Zoom out
            scale -= 0.1;
            if (scale < 1) scale = 1; // Prevent zooming out too far
        }

        lightboxImg.style.transform = `scale(${scale})`;
        lightboxImg.style.cursor = scale > 1 ? 'zoom-out' : 'zoom-in';
    });

    // Next and previous buttons for image navigation
    var next = document.querySelector('.next');
    var prev = document.querySelector('.prev');
    next.onclick = function() {
        showImage(currentImageIndex + 1);
    };
    prev.onclick = function() {
        showImage(currentImageIndex - 1);
    };

    // Keyboard navigation for next/previous image (left and right arrow keys)
    document.addEventListener('keydown', function(event) {
        if (event.key === "ArrowRight") {
            // Right arrow - Next image
            showImage(currentImageIndex + 1);
        } else if (event.key === "ArrowLeft") {
            // Left arrow - Previous image
            showImage(currentImageIndex - 1);
        }
    });
});
