# REROUTE Auth Template

<div align="center">

**JWT Authentication + REROUTE File-Based Routing**

A production-ready Cookiecutter template for FastAPI applications with complete JWT authentication, user management, and database integration.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![REROUTE](https://img.shields.io/badge/REROUTE-0.4.0%2B-green.svg)](https://github.com/cbsajan/reroute)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org)

[Features](#features) • [Quick Start](#quick-start) • [API Endpoints](#api-endpoints) • [Security](#security)

</div>

---

## Overview

**REROUTE Auth** provides a complete authentication system out of the box. Built with FastAPI and REROUTE's file-based routing, it includes JWT tokens, secure password hashing, database integration, and all the endpoints you need for user management.

**What's Included:**
- JWT authentication (access + refresh tokens)
- Secure password hashing with bcrypt
- User registration, login, token refresh, and profile endpoints
- Full database integration (PostgreSQL, MySQL, SQLite, MongoDB)
- Rate limiting and caching decorators
- Duplicate email detection
- Proper error handling with HTTP status codes
- Environment-based configuration

**Perfect for:**
- SaaS applications
- Multi-tenant systems
- API backends for frontend apps
- Mobile app backends
- Any project requiring user authentication

## Features

### Authentication
- **JWT Tokens** - Access tokens (30min) + refresh tokens (7 days)
- **Secure Password Hashing** - bcrypt with automatic salt generation
- **Token Refresh** - Seamless token renewal without re-login
- **Protected Routes** - Header-based Bearer token authentication
- **Rate Limiting** - Built-in protection against brute force attacks

### Database Integration
- **Full SQLAlchemy Support** - User model with email, password hash, name
- **Automatic Table Creation** - Database initialized on startup
- **Session Management** - Proper connection handling and cleanup
- **Duplicate Detection** - Email uniqueness validation
- **Multiple Databases** - PostgreSQL, MySQL, SQLite, MongoDB support

### Developer Experience
- **File-Based Routing** - Auto-discovered routes from directory structure
- **FastAPI Integration** - Interactive docs at `/docs`
- **Environment Configuration** - `.env` file support
- **Structured Logging** - Request logging with user context
- **Error Handling** - Proper HTTP status codes and error messages
- **OpenAPI Documentation** - Auto-generated API specs

### Security Features
- Password never stored in plain text
- JWT secret configurable via environment
- Rate limiting on sensitive endpoints (login: 5/min, register: 3/min)
- Caching on profile endpoint (60 seconds)
- CORS configuration support
- Secure token validation

## Quick Start

### Option 1: Using REROUTE CLI (Recommended)

```bash
# Install REROUTE with FastAPI support
pip install reroute[fastapi]

# Create a new auth-enabled project
reroute init my-auth-api --template gh:cbsajan/reroute-auth

# Navigate to project
cd my-auth-api

# Set up environment
cp .env.example .env
# Edit .env and update:
#   - REROUTE_DATABASE_URL (PostgreSQL connection string)
#   - REROUTE_JWT_SECRET (Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")

# Install dependencies
uv sync

# Run the server
uv run main.py
```

**Your auth API is now running at:** http://localhost:7376

Interactive API docs: http://localhost:7376/docs

### Option 2: Using Cookiecutter Directly

```bash
# Install cookiecutter
pip install cookiecutter

# Generate project
cookiecutter gh:cbsajan/reroute-auth

# Follow the prompts
cd my-auth-api
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure .env file
cp .env.example .env
# Update DATABASE_URL and JWT_SECRET

# Run
python main.py
```

## Template Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `project_name` | Name of the project | `my-auth-api` |
| `description` | Project description | `Authentication API` |
| `framework` | Backend framework | `fastapi` |
| `host` | Server host | `0.0.0.0` |
| `port` | Server port | `7376` |
| `reload` | Enable auto-reload | `true` |
| `include_tests` | Generate test files | `Yes` |
| `database` | Database type | `postgresql` |
| `jwt_secret` | JWT secret key | `CHANGE_THIS_SECRET` |
| `jwt_algorithm` | JWT algorithm | `HS256` |
| `access_token_expire_minutes` | Access token expiry | `30` |
| `refresh_token_expire_days` | Refresh token expiry | `7` |
| `package_manager` | Package manager | `uv` |

## Generated Project Structure

```
my-auth-api/
├── app/
│   ├── routes/
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── login/
│   │   │   │   └── page.py       # POST /auth/login
│   │   │   ├── register/
│   │   │   │   └── page.py       # POST /auth/register
│   │   │   ├── refresh/
│   │   │   │   └── page.py       # POST /auth/refresh
│   │   │   └── me/
│   │   │       └── page.py       # GET /auth/me (protected)
│   │   └── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py            # JWT token utilities
│   │   ├── password.py       # Password hashing
│   │   └── models.py         # Pydantic schemas
│   ├── db_models/
│   │   ├── __init__.py
│   │   └── user.py           # User database model
│   ├── database.py           # Database configuration
│   └── __init__.py
├── config.py                # Application config (includes JWT settings)
├── logger.py                # Logging setup
├── main.py                  # Application entry point
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Dependencies
└── .env.example             # Environment variables template
```

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### POST /auth/login
Authenticate and receive JWT tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /auth/refresh
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### GET /auth/me
Get current user profile (requires Bearer token).

**Headers:**
```
Authorization: Bearer eyJ...
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe"
}
```

## Next Steps

After creating a project:

```bash
cd my-auth-api

# Create virtual environment and install dependencies
uv venv
uv sync

# Copy environment file and configure
cp .env.example .env
# Edit .env and set REROUTE_JWT_SECRET to a secure value

# Run the development server
uv run main.py
```

Visit http://localhost:7376/docs for interactive API documentation.

## Security Notes

**CRITICAL Security Steps for Production:**

1. **Generate Secure JWT Secret**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Set this in your `.env` file as `REROUTE_JWT_SECRET`

2. **Use HTTPS** - Always use HTTPS in production for secure token transmission

3. **Environment Variables** - Never commit `.env` files to version control

4. **Database Security**
   - Use strong database passwords
   - Restrict database network access
   - Enable SSL for database connections

5. **CORS Configuration** - Set appropriate origins for your frontend:
   ```bash
   REROUTE_CORS_ORIGINS=https://yourdomain.com
   ```

6. **Rate Limiting** - Already configured on sensitive endpoints:
   - Login: 5 requests per minute
   - Register: 3 requests per minute
   - Refresh: 10 requests per minute

---

## Architecture

### Project Structure

```
my-auth-api/
├── app/
│   ├── routes/
│   │   └── auth/
│   │       ├── login/page.py       # POST /auth/login
│   │       ├── register/page.py    # POST /auth/register
│   │       ├── refresh/page.py     # POST /auth/refresh
│   │       └── me/page.py          # GET /auth/me (protected)
│   ├── auth/
│   │   ├── jwt.py                  # JWT token creation & validation
│   │   ├── password.py             # Password hashing with bcrypt
│   │   └── models.py               # Pydantic schemas
│   ├── db_models/
│   │   └── user.py                 # SQLAlchemy User model
│   ├── database.py                 # Database session management
│   └── __init__.py
├── config.py                       # App configuration
├── logger.py                       # Logging setup
├── main.py                         # Entry point with DB init
├── pyproject.toml                  # Python project config
├── requirements.txt                # Dependencies
└── .env.example                    # Environment template
```

### How It Works

**Registration Flow:**
1. User submits email + password + name to `POST /auth/register`
2. Password is hashed with bcrypt
3. User record created in database
4. Returns user info (without password)

**Login Flow:**
1. User submits email + password to `POST /auth/login`
2. Database lookup by email
3. Password verification with bcrypt
4. JWT tokens generated (access + refresh)
5. Returns tokens with expiry time

**Token Refresh Flow:**
1. Client sends refresh token to `POST /auth/refresh`
2. Token validated (must be refresh type, not expired)
3. New access token generated
4. Returns new access token

**Protected Endpoint Flow:**
1. Client includes `Authorization: Bearer <access_token>` header
2. Token extracted and validated
3. User ID from token used to fetch fresh user data
4. Returns user profile

---

## Database Setup

### PostgreSQL (Recommended)

```bash
# Create database
createdb my-auth-api

# Set connection string in .env
REROUTE_DATABASE_URL=postgresql://user:password@localhost:5432/my-auth-api
```

### MySQL

```bash
# Create database
mysql -u root -e "CREATE DATABASE my_auth_api;"

# Set connection string in .env
REROUTE_DATABASE_URL=mysql+pymysql://user:password@localhost:3306/my_auth_api
```

### SQLite (Development)

```bash
# Set connection string in .env
REROUTE_DATABASE_URL=sqlite:///./my-auth-api.db
```

### MongoDB

```bash
# Set connection string in .env
REROUTE_DATABASE_URL=mongodb://localhost:27017/my-auth-api
```

---

## Customization

### Changing Token Expiry

Edit `.env`:
```bash
# Access token (default: 30 minutes)
REROUTE_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Refresh token (default: 7 days)
REROUTE_REFRESH_TOKEN_EXPIRE_DAYS=30
```

### Adding User Fields

1. Update `app/db_models/user.py`:
   ```python
   class User(Base):
       # ... existing fields
       phone = Column(String(20))
       avatar_url = Column(String(255))
   ```

2. Update `app/auth/models.py`:
   ```python
   class UserRegister(BaseModel):
       # ... existing fields
       phone: Optional[str] = None
       avatar_url: Optional[str] = None
   ```

3. Run database migration or recreate tables

### Adding Custom Endpoints

Create new route files following REROUTE conventions:

```python
# app/routes/auth/forgot-password/page.py
from fastapi import Body
from reroute import RouteBase

class ForgotPasswordRoutes(RouteBase):
    def post(self, email: str = Body(...)):
        # Implement password reset logic
        return {"message": "Password reset email sent"}
```

---

## Testing

### Manual Testing with curl

```bash
# Register
curl -X POST http://localhost:7376/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123","name":"Test User"}'

# Login
curl -X POST http://localhost:7376/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123"}'

# Get profile (replace TOKEN with access_token from login)
curl http://localhost:7376/auth/me \
  -H "Authorization: Bearer TOKEN"

# Refresh token (replace REFRESH_TOKEN)
curl -X POST http://localhost:7376/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"REFRESH_TOKEN"}'
```

### Using the Interactive Docs

Visit http://localhost:7376/docs for full Swagger UI where you can:
- See all endpoints with schemas
- Test endpoints directly in browser
- View request/response models
- Download OpenAPI specification

---

## Troubleshooting

**"Database not configured" error:**
- Check `REROUTE_DATABASE_URL` in `.env`
- Ensure database server is running
- Verify connection credentials

**"Invalid or expired token" error:**
- Access tokens expire after 30 minutes
- Use refresh token to get new access token
- Check system time if tokens expire immediately

**"Email already registered" error:**
- This is expected for duplicate emails
- Use unique email addresses for testing
- Check database for existing records

**Port already in use:**
```bash
# Change port in .env
REROUTE_PORT=7377
```

---

## Production Checklist

- [ ] Generate secure `REROUTE_JWT_SECRET`
- [ ] Set `REROUTE_DEBUG=False`
- [ ] Use HTTPS for all endpoints
- [ ] Configure appropriate `REROUTE_CORS_ORIGINS`
- [ ] Use production-grade database (PostgreSQL recommended)
- [ ] Set up database backups
- [ ] Configure logging aggregation
- [ ] Set up monitoring and alerting
- [ ] Review rate limiting thresholds
- [ ] Implement account lockout after failed login attempts
- [ ] Add email verification for registration
- [ ] Implement password reset functionality
- [ ] Add 2FA/MFA support
- [ ] Regular security audits

---

## Documentation

- **REROUTE Docs**: https://cbsajan.github.io/reroute
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **JWT Best Practices**: https://tools.ietf.org/html/rfc8725

---

## Support

- **Issues**: https://github.com/cbsajan/reroute/issues
- **Discussions**: https://github.com/cbsajan/reroute/discussions
- **Documentation**: https://cbsajan.github.io/reroute

---

## License

MIT © [Sajan](https://github.com/cbsajan)
