document.addEventListener("DOMContentLoaded", function() {
    
    var countryName = document.querySelector('.country-name').textContent.trim();
    countryName = countryName.replace(/\s+/g, '_'); // Замена всех пробелов на подчеркивания
    var imagePath = '/static/flags/' + countryName + '.webp';

    var img = new Image();
    var backgroundImageElement = document.querySelector('.background-image');

    img.onload = function() {
        backgroundImageElement.style.backgroundImage = 'url(' + imagePath + ')';
        backgroundImageElement.classList.add('loaded');
    };

    img.src = imagePath;
});
