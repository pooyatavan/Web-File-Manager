    function printImage(imageId) {
        // Get the image element using the unique image ID passed as a parameter
        const imageSrc = document.getElementById(imageId).src;
        
        // Save the current page content
        const originalContent = document.body.innerHTML;

        // Create the HTML structure with only the image to print
        const tagImage = `
            <img src="${imageSrc}" style="width: 100%; height: 100%; object-fit: contain;" />
        `;
        
        // Replace the page content with just the image and apply print styles
        document.body.innerHTML = `
            <html>
                <head>
                    <style>
                        @media print {
                            body {
                                margin: 0;
                                padding: 0;
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
                    ${tagImage}
                </body>
            </html>
        `;
        
        // Trigger the print dialog
        window.print();
        
        // Restore the original page content after printing
        document.body.innerHTML = originalContent;
    }