btn.onclick = function () {
    modal.style.display = "block";
    document.body.classList.add("modal-open");
};

span.onclick = function () {
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
};

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
    }
};

document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal.style.display === "block") {
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
    }
});