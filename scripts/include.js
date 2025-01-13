// Функция для загрузки HTML-файлов
function includeHTML() {
	const elements = document.querySelectorAll("[data-include]");
	elements.forEach((el) => {
		const file = el.getAttribute("data-include");
		if (file) {
			fetch(file)
				.then(response => {
					if (response.ok) {
						return response.text();
					} else {
						throw new Error("Ошибка загрузки файла: " + file);
					}
				})
				.then(data => {
					el.innerHTML = data;
				})
				.catch(error => console.error(error));
		}
	});
}

// Запуск функции после загрузки DOM
document.addEventListener("DOMContentLoaded", includeHTML);
