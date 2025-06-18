// Image to Braille Conversion JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');
    const extractedTextElement = document.getElementById('extracted-text');
    const brailleOutputElement = document.getElementById('braille-output');
    const detailedMapping = document.getElementById('detailed-mapping');
    const languageSelect = document.getElementById('language-select');
    const uploadForm = document.getElementById('upload-form');
    const loadingSpinner = document.getElementById('loading-spinner');
    const readAloudButton = document.getElementById('read-aloud-button');
    
    // Event listener for image input change
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            // Display image preview
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.classList.remove('d-none');
            };
            
            reader.readAsDataURL(file);
        } else {
            previewContainer.classList.add('d-none');
        }
    });
    
    // Event listener for form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const file = imageInput.files[0];
        
        if (!file) {
            showNotification('Error', 'Please select an image file');
            return;
        }
        
        // Show loading spinner
        loadingSpinner.classList.remove('d-none');
        
        // Get selected language
        const language = languageSelect.value;
        
        // Create form data
        const formData = new FormData();
        formData.append('image', file);
        formData.append('language', language);
        
        // Send image to server for OCR and Braille conversion
        fetch('/api/image-to-text', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading spinner
            loadingSpinner.classList.add('d-none');
            
            if (data.error) {
                showNotification('Error', data.error);
                return;
            }
            
            // Display extracted text
            extractedTextElement.textContent = data.text;
            
            // Display Braille output
            brailleOutputElement.textContent = data.braille;
            
            // Display detailed mapping
            if (data.detailed_mapping) {
                displayDetailedMapping(data.detailed_mapping);
            }
            
            // Show read aloud button
            if (readAloudButton) {
                readAloudButton.classList.remove('d-none');
            }
            
            showNotification('Success', 'Text extracted and converted to Braille');
        })
        .catch(error => {
            // Hide loading spinner
            loadingSpinner.classList.add('d-none');
            
            console.error('Error processing image:', error);
            showNotification('Error', 'Failed to process image: ' + error.message);
        });
    });
    
    // Event listener for read aloud button
    if (readAloudButton) {
        readAloudButton.addEventListener('click', function() {
            const text = extractedTextElement.textContent;
            
            if (!text || text.trim() === '') {
                showNotification('Error', 'No text to read');
                return;
            }
            
            readAloud(text);
        });
    }
    
    // Function to read text aloud
    function readAloud(text) {
        fetch('/api/text-to-speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                showNotification('Error', data.error);
                return;
            }
            
            // Play the audio
            const audio = new Audio('data:audio/mp3;base64,' + data.audio_data);
            audio.play();
            
            showNotification('Success', 'Reading text aloud');
        })
        .catch(error => {
            console.error('Error reading text aloud:', error);
            showNotification('Error', 'Failed to read text aloud: ' + error.message);
        });
    }
    
    // Function to display detailed character mapping
    function displayDetailedMapping(mapping) {
        detailedMapping.innerHTML = '';
        
        if (!mapping || mapping.length === 0) {
            return;
        }
        
        // Create table header
        const table = document.createElement('table');
        table.className = 'table table-dark table-bordered';
        
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        const originalHeader = document.createElement('th');
        originalHeader.textContent = 'Character';
        
        const brailleHeader = document.createElement('th');
        brailleHeader.textContent = 'Braille';
        
        headerRow.appendChild(originalHeader);
        headerRow.appendChild(brailleHeader);
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Create table body
        const tbody = document.createElement('tbody');
        
        mapping.forEach(item => {
            const row = document.createElement('tr');
            
            const originalCell = document.createElement('td');
            originalCell.textContent = item.original;
            
            const brailleCell = document.createElement('td');
            brailleCell.textContent = item.braille;
            brailleCell.style.fontSize = '24px';
            
            row.appendChild(originalCell);
            row.appendChild(brailleCell);
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        detailedMapping.appendChild(table);
    }

    // Function to show notification
    function showNotification(title, message) {
        const notification = document.getElementById('notification');
        const notificationTitle = document.getElementById('notification-title');
        const notificationMessage = document.getElementById('notification-message');
        
        if (notification && notificationTitle && notificationMessage) {
            notificationTitle.textContent = title;
            notificationMessage.textContent = message;
            
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        } else {
            console.log(`Notification: ${title} - ${message}`);
        }
    }
});
