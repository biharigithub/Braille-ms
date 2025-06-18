// ✅ Updated Image to Braille Conversion JavaScript for Android WebView & Deployment Compatibility

document.addEventListener('DOMContentLoaded', function () {
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

    // Image preview
    imageInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                imagePreview.src = e.target.result;
                previewContainer.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.classList.add('d-none');
        }
    });

    // Form submit for OCR
    uploadForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const file = imageInput.files[0];
        if (!file) {
            showNotification('Error', 'Please select an image file');
            return;
        }

        loadingSpinner.classList.remove('d-none');
        const language = languageSelect.value;
        const formData = new FormData();
        formData.append('image', file);
        formData.append('language', language);

        fetch('/api/image-to-text', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.json();
        })
        .then(data => {
            loadingSpinner.classList.add('d-none');
            if (data.error) {
                showNotification('Error', data.error);
                return;
            }
            extractedTextElement.textContent = data.text;
            brailleOutputElement.textContent = data.braille;
            if (data.detailed_mapping) displayDetailedMapping(data.detailed_mapping);
            if (readAloudButton) readAloudButton.classList.remove('d-none');
            showNotification('Success', 'Text extracted and converted to Braille');
        })
        .catch(error => {
            loadingSpinner.classList.add('d-none');
            console.error('Error:', error);
            showNotification('Error', 'Image processing failed: ' + error.message);
        });
    });

    // Read Aloud using WebView-friendly speech synthesis
    if (readAloudButton) {
        readAloudButton.addEventListener('click', function () {
            const text = extractedTextElement.textContent;
            if (!text || text.trim() === '') {
                showNotification('Error', 'No text to read');
                return;
            }
            readAloud(text);
        });
    }

    function readAloud(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            speechSynthesis.speak(utterance);
            showNotification('Success', 'Reading text aloud');
        } else {
            showNotification('Error', 'Speech synthesis not supported');
        }
    }

    function displayDetailedMapping(mapping) {
        detailedMapping.innerHTML = '';
        if (!mapping || mapping.length === 0) return;

        const table = document.createElement('table');
        table.className = 'table table-dark table-bordered';

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = '<th>Character</th><th>Braille</th>';
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        mapping.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${item.original}</td><td style="font-size:24px;">${item.braille}</td>`;
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        detailedMapping.appendChild(table);
    }

    function showNotification(title, message) {
        const notification = document.getElementById('notification');
        const notificationTitle = document.getElementById('notification-title');
        const notificationMessage = document.getElementById('notification-message');

        if (notification && notificationTitle && notificationMessage) {
            notificationTitle.textContent = title;
            notificationMessage.textContent = message;
            notification.classList.add('show');
            setTimeout(() => notification.classList.remove('show'), 3000);
        } else {
            console.log(`Notification: ${title} - ${message}`);
        }
    }
});
