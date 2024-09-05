var lightbox = document.getElementById("lightbox");
var lightboxImg = document.getElementById("lightbox-img");
var captionText = document.getElementById("caption");
var currentImageIndex = 0;
var images = document.querySelectorAll('.gallery-item-image');
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
}
images.forEach((item, index) => {
    item.addEventListener('click', function() {
     
        showImage(index);
    });
});
var span = document.getElementsByClassName("close")[0];
span.onclick = function() { 
    lightbox.style.display = "none";
    lightboxImg.style.transform = "scale(1)";
}
lightboxImg.addEventListener('click', function() {
    if (lightboxImg.style.transform === "scale(1.5)") {
        lightboxImg.style.transform = "scale(1)";
        lightboxImg.style.cursor = "zoom-in";
    } else {
        lightboxImg.style.transform = "scale(1.5)";
        lightboxImg.style.cursor = "zoom-out";
    }
});
var next = document.querySelector('.next');
var prev = document.querySelector('.prev');
next.onclick = function() {
  
    showImage(currentImageIndex + 1);
}
prev.onclick = function() {
    
    showImage(currentImageIndex - 1);
}
