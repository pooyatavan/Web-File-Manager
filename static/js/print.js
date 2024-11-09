function printImage(imageId) {
    // Get the image element using the unique image ID passed as a parameter
    const imageSrc = document.getElementById(imageId).src;

    // Open a new window
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
                            width: 100%;
                            height: 100%;
                            object-fit: contain;
                        }
                    }
                </style>
            </head>
            <body>
                <img src="${imageSrc}" style="width: 100%; height: 100%; object-fit: contain;" />
            </body>
        </html>
    `);

    // Wait for the new window to finish loading, then trigger the print
    printWindow.document.close(); // Close the document stream to indicate that the writing is complete
    printWindow.focus(); // Ensure the window is focused
    printWindow.print(); // Trigger the print dialog
    printWindow.onafterprint = function () {
        printWindow.close(); // Close the print window after printing
    };
}
