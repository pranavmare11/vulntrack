# VulnTrack

A Django-based vulnerability management platform for documenting, exploring, and sharing security findings.

## About the Project

VulnTrack is a web application designed for cybersecurity enthusiasts and security researchers to document vulnerabilities, share findings, and explore security-related posts. It provides a collaborative environment for learning and managing vulnerability information.

## Features

- User authentication and profiles
- Create and share vulnerability findings
- Explore vulnerability reports
- Detailed vulnerability post pages
- Like and comment functionality
- Login-required access to protected features

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/VulnTrack.git
cd VulnTrack
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

http://127.0.0.1:8000/

## Project Structure

```text
VulnTrack/
├── manage.py
├── vulnerabilities/
├── templates/
├── static/
├── requirements.txt
└── README.md
```

*Update this structure to match your actual project files.*

## Screenshots

Add screenshots of your application here to demonstrate its interface and features.

## Future Improvements

- Search and filter vulnerability reports
- Add vulnerability severity classification
- Improve report management
- Add enhanced security features

## Disclaimer

VulnTrack is developed for educational and cybersecurity research purposes. Any security testing should be conducted only on systems where proper authorization has been obtained.

## Author

**Pranav Mare**

- GitHub: https://github.com/pranavmare11
- LinkedIn: https://linkedin.com/in/pranav-mare-343b74390/

## License

This project is licensed under the MIT License.
