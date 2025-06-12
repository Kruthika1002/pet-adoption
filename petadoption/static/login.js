async function sendData() {
    const userInput = document.getElementById('userInput').value;
    
    try {
        const response = await fetch('/api/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: userInput })
        });
        
        const result = await response.json();
        
        // Display the response
        document.getElementById('response').innerHTML = result.message;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerHTML = 'Error sending data';
    }
}

// Function to fetch data from Python backend
async function fetchData() {
    try {
        const response = await fetch('/api/get-data');
        const data = await response.json();
        
        // Display the fetched data
        const dataList = document.getElementById('dataList');
        dataList.innerHTML = ''; // Clear existing items
        
        data.items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            dataList.appendChild(li);
        });
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('dataList').innerHTML = 'Error fetching data';
    }
}

// Execute when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded and JavaScript is working!');
});