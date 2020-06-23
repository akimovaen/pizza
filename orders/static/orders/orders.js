document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.show-content').forEach(arrow => {
        arrow.onclick = function() {
            arrow.classList.toggle('open');
            const open_order = arrow.parentElement.querySelector('.open');
            if (open_order) {
                arrow.innerHTML = '&#x21F1';
                arrow.nextElementSibling.style.display = "inline";
            }
            else {
                arrow.innerHTML = '&#x21F2';
                arrow.nextElementSibling.style.display = "none";
            }
        }
    });

});