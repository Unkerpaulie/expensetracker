# Expense Tracker

A Django-based web application for tracking personal expenses and income with data visualization.

Based on the tutorial at https://www.youtube.com/watch?v=gAI218HSK8s&list=PLx-q4INfd95G-wrEjKDAcTB1K-8n1sIiz

## Features

- 📊 Dashboard with charts and data visualization
- 💰 Expense and income tracking
- 🔍 Search functionality
- 👤 User authentication
- ⚙️ User preferences (currency selection)
- 📱 Responsive design with Bootstrap 5

## Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/Unkerpaulie/expensetracker.git
cd expensetracker

# 2. Setup environment (interactive)
python setup_env.py
# Select option 1 for local development

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the application.

## Deployment

This application supports multiple deployment platforms:

- **Local Development** - SQLite database, Django dev server
- **Railway** - PostgreSQL, Gunicorn, WhiteNoise for static files
- **PythonAnywhere** - SQLite or MySQL, PythonAnywhere hosting

### Quick Deployment Links

- 📖 **[Quick Start Guide](QUICKSTART.md)** - Get started in 3 steps
- 📚 **[Full Deployment Guide](DEPLOYMENT.md)** - Detailed instructions for all platforms
- 🔄 **[Changes Documentation](CHANGES.md)** - What's new and how to migrate

### Environment Setup Helper

Use the interactive setup script to configure your environment:

```bash
python setup_env.py
```

This will help you create the appropriate `.env` file for your deployment target.

## Environment Variables

The application uses environment variables for configuration. Key variables:

- `ENVIRONMENT` - Set to `local`, `railway`, or `pythonanywhere`
- `DEBUG` - Enable/disable debug mode (`True` or `False`)
- `SECRET_KEY` - Django secret key (generate a new one for production)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - Database connection string (for Railway/PythonAnywhere)

See [`.env.example`](.env.example) for a complete list of available variables.

## Technology Stack

- **Backend:** Django 5.0.4
- **Database:** SQLite (local), PostgreSQL (Railway), MySQL (PythonAnywhere)
- **Frontend:** Bootstrap 5.3, Chart.js, Font Awesome 5.15
- **Deployment:** Gunicorn, WhiteNoise

## Project Structure

```
expensetracker/
├── authentication/     # User authentication
├── core/              # Dashboard and home
├── expenses/          # Expense management
├── income/            # Income tracking
├── preferences/       # User settings
├── reports/           # Analytics (coming soon)
├── expensetracker/    # Project settings
├── static/            # Static files
└── templates/         # HTML templates
```

## Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

### Run Tests

```bash
python manage.py test
```

## Code Snippets

### Font Awesome CDN 5.15

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
```

### Bootstrap JS 5.3

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available for educational purposes.

## Support

For deployment help, see:
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [CHANGES.md](CHANGES.md) - Recent changes and migration guide

## Acknowledgments

- Tutorial by [YouTube Channel](https://www.youtube.com/watch?v=gAI218HSK8s&list=PLx-q4INfd95G-wrEjKDAcTB1K-8n1sIiz)
- Bootstrap 5 for UI components
- Chart.js for data visualization