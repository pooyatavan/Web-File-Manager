function printImage(imageId) {
    // Get the image element using the unique image ID passed as a parameter
    const imageElement = document.getElementById(imageId);

    // Get the full-size image URL from the data-image attribute
    const mainImageSrc = imageElement.getAttribute('data-image');
    
    // Debugging: Check if the mainImageSrc is valid
    if (!mainImageSrc) {
        alert("Main image source is invalid.");
        return;
    }

    // Debugging: Log the main image source to the console
    console.log("Main Image URL:", mainImageSrc);

    // Open a new window for printing
    const printWindow = window.open('', '_blank', 'width=800,height=600');

    // Write the HTML and CSS for the print window
    printWindow.document.write(`
        <html>
            <head>
                <title>Print Image</title>
                <style>
                    @media print {
                        body {
                            margin: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }
                        img {
                            max-width: 90%;
                            max-height: 90%;
                            object-fit: contain;
                        }
                    }
                </style>
            </head>
            <body>
                <img id="print-image" src="${mainImageSrc}" alt="Image to Print" style="display:none;" />
                <script>
                    // Wait for the image to load before printing
                    const img = document.getElementById('print-image');
                    img.onload = function() {
                        // Image is fully loaded, now display and trigger the print dialog
                        img.style.display = 'block'; // Make the image visible
                        window.print();
                    }
                    img.onerror = function() {
                        alert("Failed to load the image for printing.");
                    }
                </script>
            </body>
        </html>
    `);

    // Close the document stream to indicate that the writing is complete
    printWindow.document.close(); 
    printWindow.focus(); // Ensure the window is focused

    // Close the print window after printing is done
    printWindow.onafterprint = function () {
        printWindow.close(); // Close the print window
    };
}