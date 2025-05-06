const baseURL = "http://127.0.0.1:5000";  // Flask server

// document.getElementById("apply-gaussian-btn").addEventListener("click", async () => {
//     const kernelSize = document.getElementById("kernel_size").value;

//     const response = await fetch(`${baseURL}/filter/gaussian`, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ kernel_size: kernelSize })
//     });

//     const data = await response.json();
//     document.getElementById("gaussian-result").src = `${baseURL}/${data.filtered_image_path}`;
// });


async function applyFilter(filterType) {
    const form = document.querySelector(`#${filterType}-form`);
    const formData = new FormData(form);
    
    try {
        const response = await fetch(`${baseURL}/filter/${filterType}`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to apply filter');
        }

        const data = await response.json();
        if (data.status === 'success') {
            const filteredImage = data.filtered_image;
            document.getElementById(`${filterType}-result`).src = filteredImage;
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error applying filter');
    }
}

document.getElementById("apply-gaussian-btn").addEventListener("click", function() {
    applyFilter('gaussian');
});

document.getElementById("apply-median-btn").addEventListener("click", function() {
    applyFilter('median');
});

document.getElementById("apply-hist-eq-btn").addEventListener("click", function() {
    applyFilter('hist_eq_yuv');
});

document.getElementById("apply-clahe-btn").addEventListener("click", function() {
    applyFilter('clahe');
});
