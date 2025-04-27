document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const clubData = JSON.parse(sessionStorage.getItem('club'));
    if (!clubData) {
        window.location.href = 'index.html';
        return;
    }
    
    // Set club and event info
    document.getElementById('eventName').textContent = clubData.event;
    document.getElementById('clubName').textContent = clubData.name;
    
    // Elements
    const video = document.getElementById('video');
    const scanStatus = document.getElementById('scanStatus');
    const regIdInput = document.getElementById('regId');
    const submitRegIdBtn = document.getElementById('submitRegId');
    const spotRegBtn = document.getElementById('spotRegBtn');
    const spotRegModal = document.getElementById('spotRegModal');
    const spotRegForm = document.getElementById('spotRegForm');
    const closeBtn = document.querySelector('.close-btn');
    const logoutBtn = document.getElementById('logoutBtn');
    const attendanceTable = document.getElementById('attendanceTable').querySelector('tbody');
    const cameraError = document.getElementById('cameraError');
    
    // Attendance records
    let attendanceRecords = [];
    
    // Load from localStorage if available
    try {
        const savedRecords = localStorage.getItem(`attendance_${clubData.event}`);
        if (savedRecords) {
            attendanceRecords = JSON.parse(savedRecords);
            updateAttendanceTable();
        }
    } catch (e) {
        console.error("Error loading saved records:", e);
    }
    
    // Initialize scanner
    let scanner = null;
    
    // Start camera
    async function startCamera() {
        try {
            // First try environment camera (back camera for mobile)
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'environment' } 
            });
            video.srcObject = stream;
            video.play();
            
            // Initialize QR code scanning
            scanner = new QRScanner(handleScan);
            scanner.start();
            
            scanStatus.textContent = 'Ready to scan';
            scanStatus.style.color = '#ffffff';
            cameraError.style.display = 'none';
        } catch (err) {
            console.error('Error accessing environment camera, trying user camera:', err);
            
            try {
                // Fall back to user camera (front camera)
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'user' } 
                });
                video.srcObject = stream;
                video.play();
                
                // Initialize QR code scanning
                scanner = new QRScanner(handleScan);
                scanner.start();
                
                scanStatus.textContent = 'Ready to scan (using front camera)';
                scanStatus.style.color = '#ffffff';
                cameraError.style.display = 'none';
            } catch (frontErr) {
                console.error('Error accessing any camera:', frontErr);
                scanStatus.textContent = 'Camera access denied. Use manual entry.';
                scanStatus.style.color = '#ff5555';
                cameraError.style.display = 'block';
            }
        }
    }
    
    // QR Code Scanner (placeholder for a real scanner library)
    function QRScanner(callback) {
        let scanning = false;
        let scanTimer = null;
        
        // In a real application, we would use a library like jsQR or instascan
        // to process video frames and detect QR codes.
        // This is just a placeholder that doesn't actually do anything.
        function checkForQRCode() {
            if (!scanning) return;
            
            // In a real implementation, each frame from the video would be
            // analyzed for QR codes here. We'd call the callback when one is found.
            
            // Keep the loop running
            scanTimer = setTimeout(checkForQRCode, 100);
        }
        
        return {
            start: function() {
                scanning = true;
                checkForQRCode();
                console.log("Scanner started (placeholder - no actual scanning)");
            },
            stop: function() {
                scanning = false;
                if (scanTimer) clearTimeout(scanTimer);
                console.log("Scanner stopped");
            }
        };
    }
    
    // Handle QR scan result
    function handleScan(regId) {
        scanStatus.textContent = `Scanned: ${regId}`;
        scanStatus.style.color = '#55ff55';
        
        // Process registration
        processRegistration(regId);
        
        // Reset status after 3 seconds
        setTimeout(() => {
            scanStatus.textContent = 'Ready to scan';
            scanStatus.style.color = '#ffffff';
        }, 3000);
    }
    
    // Process registration
    function processRegistration(regId, isSpotRegistration = false, userData = null) {
        // Check if already registered
        const existingRecord = attendanceRecords.find(record => record.regId === regId);
        if (existingRecord) {
            alert(`Registration ID ${regId} is already checked in!`);
            return;
        }
        
        // If not a spot registration and no user data provided,
        // in a real app we would fetch user data from the server here
        
        // Create record
        const record = {
            time: new Date().toLocaleTimeString(),
            name: userData ? `${userData.firstName} ${userData.lastName}` : 'Unknown',
            regId: regId,
            type: isSpotRegistration ? 'On-Spot' : 'Pre-Registered'
        };
        
        // Add to records
        attendanceRecords.unshift(record);
        
        // Save to localStorage
        try {
            localStorage.setItem(`attendance_${clubData.event}`, JSON.stringify(attendanceRecords));
        } catch (e) {
            console.error("Error saving records:", e);
        }
        
        // Update UI
        updateAttendanceTable();
    }
    
    // Update attendance table
    function updateAttendanceTable() {
        attendanceTable.innerHTML = '';
        
        attendanceRecords.forEach(record => {
            const row = document.createElement('tr');
            
            const timeCell = document.createElement('td');
            timeCell.textContent = record.time;
            
            const nameCell = document.createElement('td');
            nameCell.textContent = record.name;
            
            const regIdCell = document.createElement('td');
            regIdCell.textContent = record.regId;
            
            const typeCell = document.createElement('td');
            typeCell.textContent = record.type;
            if (record.type === 'On-Spot') {
                typeCell.style.color = '#ffd000';
            }
            
            row.appendChild(timeCell);
            row.appendChild(nameCell);
            row.appendChild(regIdCell);
            row.appendChild(typeCell);
            
            attendanceTable.appendChild(row);
        });
    }
    
    // Handle manual registration ID submission
    submitRegIdBtn.addEventListener('click', () => {
        const regId = regIdInput.value.trim();
        if (regId) {
            processRegistration(regId);
            regIdInput.value = '';
        } else {
            alert('Please enter a registration ID');
        }
    });
    
    // Also handle Enter key in the input field
    regIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            submitRegIdBtn.click();
        }
    });
    
    // Handle spot registration button
    spotRegBtn.addEventListener('click', () => {
        spotRegModal.style.display = 'flex';
    });
    
    // Close modal
    closeBtn.addEventListener('click', () => {
        spotRegModal.style.display = 'none';
    });
    
    // Close modal on outside click
    window.addEventListener('click', (e) => {
        if (e.target === spotRegModal) {
            spotRegModal.style.display = 'none';
        }
    });
    
    // Handle spot registration form submission
    spotRegForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const userData = {
            firstName: document.getElementById('firstName').value,
            lastName: document.getElementById('lastName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value
        };
        
        // Generate a spot registration ID
        const randomPart = Math.random().toString(36).substring(2, 6).toUpperCase();
        const spotRegId = `BTF-SPOT-${randomPart}`;
        
        // Process the registration
        processRegistration(spotRegId, true, userData);
        
        // Reset form and close modal
        spotRegForm.reset();
        spotRegModal.style.display = 'none';
    });
    
    // Handle logout
    logoutBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to logout?')) {
            // Stop scanner if active
            if (scanner) scanner.stop();
            
            // Stop video stream
            if (video.srcObject) {
                const tracks = video.srcObject.getTracks();
                tracks.forEach(track => track.stop());
            }
            
            // Clear session
            sessionStorage.removeItem('club');
            
            // Redirect to login
            window.location.href = 'index.html';
        }
    });
    
    // Start camera on page load
    startCamera();
}); 