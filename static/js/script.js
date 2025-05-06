document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const uploadBox = document.getElementById('uploadBox');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const welcomeMessage = document.getElementById('welcomeMessage');
    const originalImage = document.getElementById('originalImage');
    const enhancedImage1 = document.getElementById('enhancedImage1');
    const enhancedImage2 = document.getElementById('enhancedImage2');
    const download1 = document.getElementById('download1');
    const download2 = document.getElementById('download2');
    const sliderBeforeImg = document.getElementById('sliderBeforeImg');
    const sliderAfterImg = document.getElementById('sliderAfterImg');
    const sliderHandle = document.getElementById('sliderHandle');
    const comparisonSlider = document.getElementById('comparisonSlider');

    // These inputs must exist in your HTML
    const applyFilterButton = document.getElementById('applyFilterButton');
    const brightnessInput = document.getElementById('brightnessInput');
    const contrastInput = document.getElementById('contrastInput');
    const filterSelect = document.getElementById('filterSelect');

    // File selection by clicking the upload box
    uploadBox.addEventListener('click', function () {
        fileInput.click();
    });

    // Drag and drop functionality
    uploadBox.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadBox.style.borderColor = '#4a6cf7';
        uploadBox.style.backgroundColor = 'rgba(74, 108, 247, 0.05)';
    });

    uploadBox.addEventListener('dragleave', function () {
        uploadBox.style.borderColor = '#4a6cf7';
        uploadBox.style.backgroundColor = 'transparent';
    });

    uploadBox.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadBox.style.borderColor = '#4a6cf7';
        uploadBox.style.backgroundColor = 'transparent';

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    // Input file selection
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length) {
            handleFileUpload(fileInput.files[0]);
        }
    });

    function handleFileUpload(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        const isSCGE = file.name.toLowerCase().endsWith('.scge');

        if (!validTypes.includes(file.type) && !isSCGE) {
            alert('Please upload a valid image file (PNG, JPG, JPEG, SCGE)');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10MB limit');
            return;
        }

        welcomeMessage.style.display = 'none';
        loadingSection.style.display = 'block';

        const formData = new FormData();
        formData.append('file', file);

        // http://localhost:5000/enhance/process_image
        fetch('/enhance/process_image', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            originalImage.src = data.original;
            enhancedImage1.src = data.enhanced1;
            enhancedImage2.src = data.enhanced2;
            sliderBeforeImg.src = data.original;
            sliderAfterImg.src = data.enhanced1;

            download1.href = data.enhanced1;
            download1.download = 'enhanced1_' + file.name;
            download2.href = data.enhanced2;
            download2.download = 'enhanced2_' + file.name;

            loadingSection.style.display = 'none';
            resultsSection.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing the image: ' + error.message);
            loadingSection.style.display = 'none';
            welcomeMessage.style.display = 'block';
        });
    }

    // Apply filters and adjustments
    applyFilterButton.addEventListener('click', function () {
        const brightness = parseInt(brightnessInput.value, 10);
        const contrast = parseInt(contrastInput.value, 10);
        const selectedFilter = filterSelect.value;

        const formData = new FormData();
        formData.append('brightness', brightness);
        formData.append('contrast', contrast);
        formData.append('filter', selectedFilter);

        fetch('/apply_adjustments', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Adjustment error: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                enhancedImage1.src = data.enhanced1;
                enhancedImage2.src = data.enhanced2;
                sliderBeforeImg.src = data.original;
                sliderAfterImg.src = data.enhanced1;
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
    });

    // Comparison slider functionality
    let isDragging = false;

    sliderHandle.addEventListener('mousedown', function (e) {
        isDragging = true;
        e.preventDefault();
    });

    document.addEventListener('mouseup', function () {
        isDragging = false;
    });

    document.addEventListener('mousemove', function (e) {
        if (!isDragging) return;

        const sliderRect = comparisonSlider.getBoundingClientRect();
        let position = (e.clientX - sliderRect.left) / sliderRect.width;
        position = Math.max(0, Math.min(1, position));

        sliderHandle.style.left = position * 100 + '%';
        document.querySelector('.slider-before').style.width = position * 100 + '%';
    });

    // Touch support
    sliderHandle.addEventListener('touchstart', function () {
        isDragging = true;
    });

    document.addEventListener('touchend', function () {
        isDragging = false;
    });

    document.addEventListener('touchmove', function (e) {
        if (!isDragging) return;

        const touch = e.touches[0];
        const sliderRect = comparisonSlider.getBoundingClientRect();
        let position = (touch.clientX - sliderRect.left) / sliderRect.width;
        position = Math.max(0, Math.min(1, position));

        sliderHandle.style.left = position * 100 + '%';
        document.querySelector('.slider-before').style.width = position * 100 + '%';
    });
});

