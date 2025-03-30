document.addEventListener('DOMContentLoaded', function() {
    const otherPowerInput = document.getElementById('other-power');
    const totalPowerDisplay = document.getElementById('total-power');
    const gpuSelect = document.getElementById('gpu');
    // const totalPowerConsumptionDisplay = document.getElementById('total-power-consumption');  // Убрал, если он не существует

    function updatePower() {
        let otherPower = parseInt(otherPowerInput.value) || 0;
        let gpuPower = 0;

        // Получаем выбранный GPU и его мощность (предполагаем, что у каждого option есть data-power)
        if (gpuSelect.value) {
            const selectedOption = gpuSelect.options[gpuSelect.selectedIndex];
            gpuPower = parseInt(selectedOption.dataset.power) || 0; // Получаем значение data-power
        }

        let totalPower = otherPower + gpuPower;
        totalPowerDisplay.textContent = `Общая мощность: ${totalPower} Вт`;
        // if (totalPowerConsumptionDisplay) {   //Проверка на существование элемента
        // totalPowerConsumptionDisplay.textContent = `${totalPower}W`; // Обновляем Build Summary
        // }
    }

    // Вызываем updatePower один раз при загрузке страницы, чтобы отобразить начальное значение
    updatePower();

    otherPowerInput.addEventListener('input', updatePower);
    gpuSelect.addEventListener('change', updatePower);
});

