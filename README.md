📌 Ważne informacje dotyczące konfiguracji i działania

1. Plik .env i dane poufne
	•	Brak pliku .env w repozytorium – celowo.
	•	Wszystkie dane poufne (np. dane do bazy PostgreSQL, klucze reCAPTCHA, itp.) są trzymane w konfiguracji Gunicorna lub środowisku serwera, nie w żadnym pliku .env.
	•	Te dane (login, hasło, klucze) wyślę Ci mailowo – nie są publikowane tutaj.

⸻

2. Renderowanie formularzy w HTML (CSRF + context)
	•	Każdy formularz HTML musi zawierać {% csrf_token %} w środku <form> – to zabezpieczenie Django.
	•	Jeżeli tworzysz widok np. do index.html, musisz zadbać, aby przekazać do szablonu oba formularze (reg_form i login_form) – inaczej nie będą działać.

Przykład widoku:

def index(request):
    return render(request, "index.html", {
        "reg_form": RegistrationForm(),
        "login_form": LoginForm(),
    })

    To pozwala na prawidłowe wyświetlenie formularzy w HTML za pomocą {{ reg_form }} i {{ login_form }}.

    3. Plik views.py
	•	Plik views.py, który Ci wysłałem, możesz wkleić 1:1 – cały kod działa.
	•	Jeśli pojawią się błędy na serwerze, to nie są one winą widoków, tylko mogą wynikać z:
	•	starego procesu Gunicorn (należy zrestartować),
	•	błędów składniowych,
	•	cache przeglądarki lub serwera.
