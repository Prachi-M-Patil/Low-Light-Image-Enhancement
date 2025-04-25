document.addEventListener('DOMContentLoaded', function() {
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
    
    // Handle file selection by clicking on the upload box
    uploadBox.addEventListener('click', function() {
        fileInput.click();
    });
    
    // Handle drag and drop
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadBox.style.borderColor = '#4a6cf7';
        uploadBox.style.backgroundColor = 'rgba(74, 108, 247, 0.05)';
    });
    
    uploadBox.addEventListener('dragleave', function() {
        uploadBox.style.borderColor = '#4a6cf7';
        uploadBox.style.backgroundColor = 'transparent';
    });
    
    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadBox.style.borderColor = '#4a6cf7';
        uploadBox.style.backgroundColor = 'transparent';
        
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
    
    // Handle file selection via input
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length) {
            handleFileUpload(fileInput.files[0]);
        }
    });
    
    // Handle the file upload process
    function handleFileUpload(file) {
        // Check if file is an image
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/scge'];
        if (!validTypes.includes(file.type) && !file.name.endsWith('.scge')) {
            alert('Please upload a valid image file (PNG, JPG, JPEG, SCGE)');
            return;
        }
        
        // Check file size (10MB max)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10MB limit');
            return;
        }
        
        // Show loading indicator
        welcomeMessage.style.display = 'none';
        loadingSection.style.display = 'block';
        
        // Create form data to send to server
        const formData = new FormData();
        formData.append('file', file);
        
        // Send file to server for processing
        fetch('/process_image', {
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
            // Handle successful response
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display the images
            originalImage.src = data.original;
            enhancedImage1.src = data.enhanced1;
            enhancedImage2.src = data.enhanced2;
            sliderBeforeImg.src = data.original;
            sliderAfterImg.src = data.enhanced1;
            
            // Setup download links
            download1.href = data.enhanced1;
            download1.download = 'enhanced1_' + file.name;
            download2.href = data.enhanced2;
            download2.download = 'enhanced2_' + file.name;
            
            // Hide loading and show results
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
    
    // Comparison slider functionality
    let isDragging = false;
    
    sliderHandle.addEventListener('mousedown', function(e) {
        isDragging = true;
        e.preventDefault();
    });
    
    document.addEventListener('mouseup', function() {
        isDragging = false;
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const sliderRect = comparisonSlider.getBoundingClientRect();
        let position = (e.clientX - sliderRect.left) / sliderRect.width;
        
        // Constrain position between 0 and 1
        position = Math.max(0, Math.min(1, position));
        
        // Update slider position
        sliderHandle.style.left = position * 100 + '%';
        document.querySelector('.slider-before').style.width = position * 100 + '%';
    });
    
    // Touch support for mobile devices
    sliderHandle.addEventListener('touchstart', function(e) {
        isDragging = true;
    });
    
    document.addEventListener('touchend', function() {
        isDragging = false;
    });
    
    document.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        
        const touch = e.touches[0];
        const sliderRect = comparisonSlider.getBoundingClientRect();
        let position = (touch.clientX - sliderRect.left) / sliderRect.width;
        
        // Constrain position between 0 and 1
        position = Math.max(0, Math.min(1, position));
        
        // Update slider position
        sliderHandle.style.left = position * 100 + '%';
        document.querySelector('.slider-before').style.width = position * 100 + '%';
    });
});