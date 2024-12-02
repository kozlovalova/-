const API_BASE_URL = "http://127.0.0.1:5000"; // Адрес API

// Валидация формы перед отправкой
document.getElementById("booking-form").addEventListener("submit", async (event) => {
  event.preventDefault(); // Предотвращаем стандартное поведение формы
  const form = event.target;

  // Клиентская валидация
  if (!form.checkValidity()) {
    form.classList.add("was-validated");
    return;
  }

  // Сбор данных формы
  const tourId = document.getElementById("tour-id").value;
  const name = document.getElementById("name").value;
  const seats = document.getElementById("seats").value;

  try {
    // Отправка POST-запроса на сервер
    const response = await axios.post("${API_BASE_URL}/book", {
      tour_id: parseInt(tourId),
      name: name.trim(),
      seats: parseInt(seats),
    });

    // Показ успешного сообщения
    document.getElementById("response-message").innerHTML = `
      <div class="alert alert-success">
        Бронирование успешно создано! ID бронирования: ${response.data.id}
      </div>
    `;
    form.reset();
    form.classList.remove("was-validated");
  } catch (error) {
    // Обработка ошибок
    const errorMessage =
      error.response && error.response.data.error
        ? error.response.data.error
        : "Не удалось создать бронирование.";
    document.getElementById("response-message").innerHTML = `
      <div class="alert alert-danger">${errorMessage}</div>
    `;
  }
});
async function fetchTours() {
    try {
      const response = await axios.get("${API_BASE_URL}/tours");
      const tours = response.data;
      const toursList = document.getElementById("tours-list");
      toursList.innerHTML = ""; // Очистка списка перед обновлением
  
      tours.forEach((tour) => {
        const tourCard = document.createElement("div");
        tourCard.className = "col-md-4";
        tourCard.innerHTML = `
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">${tour.name}</h5>
              <p class="card-text">Цена: ${tour.price} $</p>
              <p class="card-text">Доступные места: ${tour.available_seats}</p>
              <p class="card-text">ID: ${tour.id}</p>
            </div>
          </div>
        `;
        toursList.appendChild(tourCard);
      });
    } catch (error) {
      console.error("Ошибка при загрузке туров:", error);
    }
  }
  
  // Обновляем список туров после успешного бронирования
  document.getElementById("booking-form").addEventListener("submit", async () => {
    await fetchTours();
  });