async function fetchParkingData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/spots');
        const data = await response.json();
        let available = 0;
        let occupied = 0;
        Object.entries(data).forEach(([spotId, status]) => {
            const isAvailable = status === "available";
            if (isAvailable) 
                {
                    available++;}
            else {occupied++;}
            const spotCard = document.querySelector(`#${spotId}`);
            if (spotCard) {
                spotCard.className = `spot w-full md:w-1/5 text-center transform transition-all duration-300 hover:translate-y-1 hover:shadow-2xl rounded-lg shadow-xl border-l-8 p-6 ${
                    isAvailable 
                        ? 'bg-gradient-to-br from-green-100 to-green-200 border-green-500'
                        : 'bg-gradient-to-br from-red-100 to-red-200 border-red-500'
                }`;

                const statusElement = spotCard.querySelector('.status-text');
                if (statusElement) {
                    statusElement.textContent = isAvailable ? "Available" : "Occupied";
                    statusElement.className = `status-text font-bold text-xl mt-2 ${
                        isAvailable ? 'text-green-600' : 'text-red-600'
                    }`;
                }

                const badge = spotCard.querySelector('.badge');
                if (badge) {
                    badge.className = `badge inline-block font-bold rounded-full w-8 h-8 flex items-center justify-center ${
                        isAvailable ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                    }`;
                }
            }
        });
        document.getElementById('available-count').textContent = available;
        document.getElementById('occupied-count').textContent = occupied;

    } catch (error) {
        console.error('Error fetching spot data:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchParkingData();
    setInterval(fetchParkingData, 1000);
});

window.addEventListener('beforeunload', () => {
    console.log('Page is about to reload!');
});