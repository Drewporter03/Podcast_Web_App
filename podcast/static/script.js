let lightMode = localStorage.getItem('lightMode');
const lightModeToggle = document.querySelector('#light-mode');
const themeName = document.getElementById("light-mode")

const enableLightMode = () => {
    document.body.classList.add('lightMode');
    localStorage.setItem('lightMode', 'enabled');
}
const disableLightMode = () => {
    document.body.classList.remove('lightMode');
    localStorage.setItem('lightMode', null);
}

if (lightMode === 'enabled') {
    enableLightMode();
    themeName.innerHTML = "Light Theme"
}

lightModeToggle.addEventListener('click', () => {
    lightMode = localStorage.getItem('lightMode');
    if (lightMode !== 'enabled') {
        enableLightMode();
        console.log(lightMode);
        themeName.innerHTML = "Light Theme"
    } else {
        disableLightMode();
        themeName.innerHTML = "Dark Theme"
    }
});
