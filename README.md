![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![psql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
# Projekt z przedmiotu "Inżyneria oprogramowania"

### Nazwa: Firma taksówkarska

Skład zespołu:
* Mateusz Szczygłów (szef)
* Krzysztof Wysocki
* Dawid Zagórski
* Patryk Szczepański

## Uruchomienie

Projekt używa Django 6.1 oraz Pythona 3.12–3.15. Domyślną bazą jest SQLite;
sterownik PostgreSQL jest również dołączony w zależnościach.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements_dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

W panelu `/admin/` dodaj dyspozytorów i kierowców. Panel dyspozytora znajduje się
pod `/panel-dyspozytora/`, a widok kierowcy pod `/<id-kierowcy>/`.
Opcjonalną konfigurację PostgreSQL można przygotować, kopiując
`project/settings_local.example` do `project/settings_local.py`.
Na potrzeby samego uruchomienia aplikacji wystarczy `requirements.txt`.

## Testy i CI

```sh
python manage.py check --settings=project.settings_test
python manage.py makemigrations --check --dry-run --settings=project.settings_test
python -m pytest --cov=taxi --cov=mobile --cov-report=term-missing
```

Testy używają osobnej bazy SQLite w pamięci i nie modyfikują lokalnej bazy.
Obejmują statusy i dostępność kierowców, formularze, tworzenie zleceń,
zgłaszanie obecności kierowcy oraz widoki aplikacji.

Workflow `.github/workflows/tests.yml` wykonuje kontrole Django, sprawdzenie
migracji i testy z pokryciem kodu w macierzy Python **3.12, 3.13, 3.14, 3.15**
po każdym pushu, pull requeście i po ręcznym uruchomieniu.
Kod w `old/` stanowi archiwalny prototyp i nie jest częścią testów Django.
