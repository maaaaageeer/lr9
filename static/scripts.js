const apiBaseUrl = '/api'; // Базовый URL API


// Функция для входа
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const loginMessage = document.getElementById('login-message');
      const errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.style.display = "none";

    try {
        const response = await fetch(`${apiBaseUrl}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.token); // Сохраняем токен
            console.log(data.token);
            loginMessage.textContent = "";
            document.getElementById('auth-form').style.display = 'none';
            fetchBonusInfo();
            document.getElementById('bonus-info').style.display = 'block';
        } else {
            const errorData = await response.json();
             loginMessage.textContent = errorData.message;
        }
    } catch (error) {
         errorMessageDiv.style.display = "block";
        errorMessageDiv.textContent = `Error: ${error}`;
    }
}


// Функция для получения данных о бонусах
async function fetchBonusInfo() {
    const token = localStorage.getItem('token');
      const errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.style.display = "none";

    if (!token) {
         errorMessageDiv.style.display = "block";
        errorMessageDiv.textContent = "Необходимо войти.";
        document.getElementById('auth-form').style.display = 'block';
        document.getElementById('bonus-info').style.display = 'none';
        return;
    }
    try {
        const response = await fetch(`${apiBaseUrl}/bonuses/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                  'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
             const data = await response.json();

            document.getElementById('current-level').textContent = data.current_level;
            document.getElementById('cashback-percentage').textContent = data.cashback_percentage;
            document.getElementById('next-level').textContent = data.next_level;
            document.getElementById('next-level-threshold').textContent = data.next_level_threshold;
             document.getElementById('current-spending').textContent = data.current_spending;

        } else {
              localStorage.removeItem('token');
             errorMessageDiv.style.display = "block";
              const errorData = await response.json();
               if (errorData.detail && errorData.detail.includes("Срок действия токена истек")) {
                    errorMessageDiv.textContent =  `Срок действия токена истек. Пожалуйста, войдите снова.`
                }
                else{
                     errorMessageDiv.textContent =  `Ошибка получения данных: ${errorData.detail || response.statusText}`
                }
           document.getElementById('auth-form').style.display = 'block';
           document.getElementById('bonus-info').style.display = 'none';
           return;
        }
    } catch (error) {
         errorMessageDiv.style.display = "block";
        errorMessageDiv.textContent = `Error: ${error}`;
    }
}


function logout(){
    localStorage.removeItem('token');
    document.getElementById('auth-form').style.display = 'block';
    document.getElementById('bonus-info').style.display = 'none';
}


// Вызвать fetchBonusInfo при загрузке страницы, чтобы проверить сохраненный токен
window.onload = fetchBonusInfo;