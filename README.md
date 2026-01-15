# ExpressYourself

A full-featured e-commerce platform built with Django and Django REST Framework. ExpressYourself provides a comprehensive solution for managing products, orders, users, and payments with a modern API-first architecture.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Features

- **Product Management**: Create, update, and manage products with images and categorization
- **Order Processing**: Complete order management system with status tracking
- **User Management**: User authentication and profile management
- **Payment Integration**: Integrated payment processing and payment status tracking
- **QR Codes**: Automatic QR code generation for orders
- **API Authentication**: JWT-based authentication for API endpoints
- **CORS Support**: Cross-origin resource sharing enabled for API access
- **Admin Interface**: Django admin panel for managing all aspects of the application
- **Search & Filtering**: Advanced product search and filtering capabilities
- **Order Tracking**: Real-time order status updates and delivery tracking

## Project Structure

```
ExpressYourself/
├── ExpressYourself/          # Main project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL router
│   ├── asgi.py               # ASGI configuration
│   └── wsgi.py               # WSGI configuration
├── store/                    # E-commerce application
│   ├── models/               # Database models
│   │   ├── product.py        # Product model
│   │   ├── order.py          # Order model
│   │   └── catagory.py       # Category model
│   ├── api/                  # REST API
│   │   ├── views.py          # API views
│   │   ├── serializers.py    # API serializers
│   │   ├── permissions.py    # API permissions
│   │   └── urls.py           # API routing
│   ├── views/                # Web views
│   ├── templates/            # HTML templates
│   └── migrations/           # Database migrations
├── users/                    # User management application
│   ├── models.py             # User models
│   ├── views.py              # User views
│   ├── forms.py              # User forms
│   ├── validators.py         # Custom validators
│   └── signals.py            # Django signals
├── utilities/                # Utility functions
│   ├── payment_module.py     # Payment processing
│   ├── qr.py                 # QR code generation
│   ├── otp.py                # OTP functionality
│   └── models.py             # Utility models
├── static/                   # Static files (CSS, JS, images)
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   └── fonts/                # Font files
├── media/                    # User-uploaded media
│   └── product_images/       # Product images
├── templates/                # Global templates
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── .gitignore                # Git ignore rules
```

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Key Dependencies

- **Django 5.0.6**: Web framework
- **Django REST Framework 3.15.2**: RESTful API framework
- **djangorestframework-simplejwt 5.3.1**: JWT authentication
- **Pillow 10.4.0**: Image processing
- **qrcode 7.4.2**: QR code generation
- **pyzbar 0.1.9**: QR code reading
- **opencv-python 4.10.0.84**: Computer vision library
- **python-dotenv 1.0.1**: Environment variable management
- **django-cors-headers 4.4.0**: CORS support

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ExpressYourself
```

### 2. Create a Virtual Environment

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies (if needed)

For QR code scanning features:

```bash
# On Ubuntu/Debian
sudo apt-get install libzbar0

# On macOS
brew install zbar
```

## Setup Instructions

### 1. Database Configuration

Initialize the database with migrations:

```bash
# Apply all migrations
python manage.py migrate

# If you need to create migrations for any changes
python manage.py makemigrations
python manage.py migrate
```

### 2. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account with username, email, and password.

### 3. Environment Variables

Create a `.env` file in the project root directory (optional, for sensitive configuration):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Note**: The project currently has `DEBUG=True` in settings. Update this for production deployments.

### 4. Collect Static Files (for production)

```bash
python manage.py collectstatic --noinput
```

### 5. Load Initial Data (Optional)

If you have data fixtures or initial data:

```bash
python manage.py loaddata fixture_name
```

## Usage Instructions

### Running the Development Server

Start the development server:

```bash
python manage.py runserver
```

The application will be available at:
- **Web Interface**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin`
- **API Root**: `http://localhost:8000/api`

### Accessing the Admin Panel

1. Navigate to `http://localhost:8000/admin`
2. Log in with your superuser credentials
3. Manage products, orders, users, and other data

### API Endpoints

The application provides comprehensive REST API endpoints:

- **Products**: `/api/products/`
- **Orders**: `/api/orders/`
- **Categories**: `/api/categories/`
- **Users**: `/api/users/`

### Authentication

The API uses JWT (JSON Web Token) authentication:

1. **Obtain Token**:
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **Use Token**: Include the token in request headers:
   ```bash
   curl -H "Authorization: Bearer your_token_here" \
     http://localhost:8000/api/products/
   ```

### Creating Products

1. Log in to admin panel or use the API
2. Navigate to Products
3. Click "Add Product"
4. Fill in required fields:
   - Name
   - Description
   - Price
   - Category
   - Product Image
   - Status
5. Save

### Processing Orders

1. Orders are created through the web interface or API
2. Track order status: Pending → Processing → Delivered
3. QR codes are automatically generated for each order
4. Payments are processed through the integrated payment module

### Managing Users

1. Users can register through the application
2. Admin can manage user accounts in the admin panel
3. User profiles can be updated with custom validators

## API Documentation

### Product Endpoints

**List Products**:
```
GET /api/products/
```

**Retrieve Product**:
```
GET /api/products/{id}/
```

**Create Product** (Admin only):
```
POST /api/products/
Content-Type: application/json

{
  "name": "Product Name",
  "description": "Description",
  "price": "29.99",
  "category": 1,
  "picture": "image_file",
  "status": "active"
}
```

**Update Product** (Admin only):
```
PATCH /api/products/{id}/
```

**Delete Product** (Admin only):
```
DELETE /api/products/{id}/
```

### Order Endpoints

**List Orders**:
```
GET /api/orders/
```

**Create Order**:
```
POST /api/orders/
Content-Type: application/json

{
  "user": 1,
  "items": [
    {"product": 1, "quantity": 2}
  ]
}
```

**Track Order**:
```
GET /api/orders/{id}/
```

## Configuration

### Settings Overview

Key settings in `ExpressYourself/settings.py`:

- **DEBUG**: Set to `False` for production
- **ALLOWED_HOSTS**: Add your domain names here
- **INSTALLED_APPS**: Registered Django apps
- **DATABASES**: Database configuration (default: SQLite)
- **REST_FRAMEWORK**: API configuration and pagination settings
- **CORS_ALLOWED_ORIGINS**: Allowed cross-origin domains

### Database Configuration

By default, the project uses SQLite. To use PostgreSQL or MySQL:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'express_yourself',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Troubleshooting

### Common Issues

**1. Migration Errors**

```bash
# Reset migrations (development only)
python manage.py migrate store zero
python manage.py migrate users zero
python manage.py migrate utilities zero

# Reapply migrations
python manage.py migrate
```

**2. Static Files Not Loading**

```bash
python manage.py collectstatic --clear --noinput
```

**3. Permission Denied Errors**

Ensure proper file permissions:
```bash
chmod +x manage.py
chmod -R 755 media/
chmod -R 755 static/
```

**4. Port Already in Use**

Run on a different port:
```bash
python manage.py runserver 8001
```

**5. QR Code Dependencies Missing**

```bash
pip install --upgrade pyzbar
pip install --upgrade qrcode[pil]
```

### Checking Logs

Django automatically logs information. Check for issues in:
- Console output when running `runserver`
- Database logs
- Application error handlers

## Production Deployment

Before deploying to production:

1. **Update Security Settings**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Use Environment Variables**: Store sensitive data in `.env` file

3. **Configure Static/Media Serving**: Use a web server like Nginx

4. **Database**: Switch to PostgreSQL or MySQL

5. **HTTPS**: Enable SSL/TLS certificates

6. **WSGI Server**: Use Gunicorn or uWSGI

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn ExpressYourself.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or suggestions, please open an issue in the repository or contact the development team.

---

**Last Updated**: January 2026
