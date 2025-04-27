document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    // Mock club credentials (in a real app, this would be verified server-side)
    const clubs = [
        { username: 'lug', password: 'lugbtf', name: 'Linux Users Group', event: 'Crack The Penguin' },
        { username: 'gdg', password: 'gdgbtf', name: 'Google Developer Group', event: 'Hunter AI' },
        { username: 'skyline', password: 'skylinebtf', name: 'Skyline', event: 'Marshmallow Tower Challenge' },
        { username: 'ieee', password: 'ieeebtf', name: 'IEEE', event: 'Research Paper Presentation' },
        { username: 'acm', password: 'acmbtf', name: 'ACM', event: 'Escape The Matrix' },
        { username: 'aiche', password: 'aichebtf', name: 'AIChE', event: 'Hydro Purity Quest' },
    ];
    
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Find matching club
        const club = clubs.find(c => c.username === username && c.password === password);
        
        if (club) {
            // Store club info in session storage
            sessionStorage.setItem('club', JSON.stringify({
                name: club.name,
                event: club.event
            }));
            
            // Redirect to scanner page
            window.location.href = 'scanner.html';
        } else {
            alert('Invalid username or password. Please try again.');
        }
    });
}); 