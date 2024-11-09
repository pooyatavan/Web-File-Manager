// Event listener for category change
$(document).ready(function() {
    $("#selectuser").change(function() {
        let selectedCategory = $(this).val();
        $.ajax({
            type: "POST",
            url: "/get_options",
            contentType: "application/json",
            data: JSON.stringify({ SelectUser: selectedCategory }),
            success: function(response) {
                let container = $("#checkbox-container");
                container.empty(); // Clear existing checkboxes

                response.forEach(function(option) {
                    // Name attribute allows data to be sent in form submission
                    let checkbox = `<label><input type="checkbox" name="options" value="${option}"> ${option}</label><br>`;
                    container.append(checkbox);
                });
            }
        });
    });
});