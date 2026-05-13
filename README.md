# E-Commerce REST API Platform

A production-oriented REST API backend for a modern e-commerce platform built with Django REST Framework. The system handles product catalog management, order processing, payment integration, and asynchronous task execution.

## 🎯 Features

### Product Management
- **Product CRUD Operations** - Create, read, update, and delete products
- **Category System** - Hierarchical product categorization
- **Stock Management** - Track inventory with replenish/reduce functionality
- **Flash Sales** - Time-based promotional campaigns
- **Product Analytics** - View history tracking for user behavior analysis
- **Product Reviews** - User rating and review system

### Order & Payment Processing
- **Order Management** - Complete order lifecycle (creation, tracking, fulfillment)
- **Stripe Payment Integration** - Secure card payment processing
- **Payment Records** - Persistent transaction history for auditing
- **Order Notifications** - Async email notifications via Celery

### Authentication & Security
- **JWT Authentication** - Stateless token-based authentication
- **Role-Based Access Control** - Custom permission system
- **User Management** - Registration and profile management
- **Environment Configuration** - Secure .env-based secrets management

### Infrastructure
- **Asynchronous Processing** - Celery workers for background tasks
- **Message Broker** - RabbitMQ for job queuing
- **Caching Layer** - Redis for performance optimization
- **Containerization** - Docker & docker-compose for consistent deployment
- **API Documentation** - Auto-generated Swagger/OpenAPI documentation

## 🛠️ Technology Stack

| Component            | Technology                             |
|----------------------|----------------------------------------|
| **Framework**        | Django 5.2, Django REST Framework 3.16 |
| **Database**         | PostgreSQL 16                          |
| **Authentication**   | JWT (djangorestframework-simplejwt)    |
| **Task Queue**       | Celery + RabbitMQ                      |
| **Cache**            | Redis                                  |
| **Payment**          | Stripe API                             |
| **Documentation**    | drf-yasg (Swagger/OpenAPI)             |
| **Containerization** | Docker, docker-compose                 |
| **Python**           | 3.11+                                  |

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16
- Redis
- RabbitMQ

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/ali-hidirov-09/E_commerse.git
cd E_commerse

# Create environment file
cp .env.example .env

# Build and start all services
docker-compose up -d

# Run database migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
API: http://localhost:8000/api/
Admin: http://localhost:8000/admin/
Swagger: http://localhost:8000/api/schema/swagger/


E_commerse/
├── config/                 # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI config
│   └── celery.py          # Celery configuration
├── products/              # Products app
│   ├── models.py          # Product, Category, Review models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── filters.py         # Query filtering
│   └── urls.py            # Product endpoints
├── billing/               # Billing/Orders app
│   ├── models.py          # Order, Payment models
│   ├── serializers.py     # Order serializers
│   ├── views.py           # Order API views
│   ├── tasks.py           # Celery tasks
│   └── urls.py            # Order endpoints
├── users/                 # Users app
│   ├── models.py          # User profile models
│   ├── serializers.py     # User serializers
│   └── views.py           # User API views
├── docker-compose.yml     # Multi-container orchestration
├── Dockerfile             # Docker image configuration
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file


# API documentation:
# Products
GET    /api/v1/products/              - List all products
GET    /api/v1/products/{id}/         - Get product details
POST   /api/v1/products/              - Create product (admin only)
PATCH  /api/v1/products/{id}/         - Update product (admin only)
DELETE /api/v1/products/{id}/         - Delete product (admin only)
GET    /api/v1/categories/            - List product categories
GET    /api/v1/products/{id}/reviews/ - Get product reviews
POST   /api/v1/products/{id}/reviews/ - Add review (authenticated)

# Order
GET    /api/v1/orders/                - List user's orders (authenticated)
POST   /api/v1/orders/                - Create new order (authenticated)
GET    /api/v1/orders/{id}/           - Get order details (authenticated)
PATCH  /api/v1/orders/{id}/           - Update order status (admin only)

# Auth
POST   /api/v1/auth/token/            - Get JWT token
POST   /api/v1/auth/token/refresh/    - Refresh JWT token
POST   /api/v1/auth/register/         - User registration

#    Payment
POST   /api/v1/payments/              - Process payment via Stripe
GET    /api/v1/payments/{id}/         - Get payment details