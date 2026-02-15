# 🎮 Gamified Machine Learning Learning Platform

A production-ready, gamified platform for learning Machine Learning through interactive quests, automated model evaluation, and achievement tracking.

## 🌟 Features

### Core Features
- ✅ **User Authentication** - JWT-based secure authentication
- 🎯 **Quest System** - Structured ML learning path with levels and quests
- 🤖 **Automated Model Evaluation** - Generic evaluation engine for any ML model
- 🏆 **Achievements & Badges** - Earn badges based on XP, streaks, and performance
- 📊 **Leaderboard** - Global rankings by XP and completed quests
- 🔥 **Daily Streaks** - Track consecutive days of learning
- 📈 **Progress Tracking** - Detailed user progress and statistics

### Technical Features
- 🏗️ **Clean Architecture** - Modular, scalable, maintainable code
- 🔐 **Secure** - Password hashing, JWT tokens, input validation
- 📦 **Docker Support** - Easy deployment with Docker/Docker Compose
- 📚 **API Documentation** - Auto-generated with FastAPI (Swagger UI)
- 🧪 **Testable** - Comprehensive test suite included

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  (Browser, Mobile App, API Client, Streamlit Dashboard)     │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
┌───────────────────────────▼─────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Routes    │  │  Services   │  │  ML Engine  │        │
│  │  (API       │──│  (Business  │──│  (Model     │        │
│  │  Endpoints) │  │   Logic)    │  │  Evaluation)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                 │                                  │
│         └─────────────────┼──────────────┐                  │
│                           ▼              ▼                  │
│                    ┌──────────────┐  ┌──────────────┐      │
│                    │   Models     │  │   Schemas    │      │
│                    │ (SQLAlchemy) │  │  (Pydantic)  │      │
│                    └──────┬───────┘  └──────────────┘      │
└───────────────────────────┼─────────────────────────────────┘
                            ▼
                    ┌──────────────┐
                    │   Database   │
                    │   (SQLite)   │
                    └──────────────┘
```

### Directory Structure

```
ml_game_platform/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py          # User model with XP/level logic
│   │   ├── level.py         # Learning level model
│   │   ├── quest.py         # Quest model with evaluation config
│   │   ├── submission.py    # User submission tracking
│   │   ├── badge.py         # Badge/achievement model
│   │   └── user_badge.py    # Many-to-many relationship
│   ├── routes/              # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── quests.py        # Quest management endpoints
│   │   ├── user.py          # User profile endpoints
│   │   ├── leaderboard.py   # Leaderboard endpoints
│   │   └── dependencies.py  # Shared dependencies (auth middleware)
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py      # Authentication & JWT
│   │   ├── quest_service.py     # Quest management
│   │   ├── badge_service.py     # Badge awarding logic
│   │   └── leaderboard_service.py # Ranking logic
│   └── ml_engine/           # ML evaluation engine
│       └── evaluator.py     # Generic model evaluation
├── datasets/                # Training datasets
├── uploads/                 # User-uploaded models
├── sample_models/          # Pre-trained sample models
├── init_db.py              # Database initialization script
├── generate_datasets.py    # Dataset generation script
├── train_sample_models.py  # Sample model training
├── test_api.py             # API test suite
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container config
├── docker-compose.yml      # Docker Compose config
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- (Optional) Docker & Docker Compose

### Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ml_game_platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and set SECRET_KEY
```

5. **Initialize database**
```bash
python init_db.py
```

6. **Generate sample datasets**
```bash
python generate_datasets.py
```

7. **Train sample models (optional)**
```bash
python train_sample_models.py
```

8. **Run the server**
```bash
uvicorn app.main:app --reload
```

9. **Access the API**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

10. **Run the Frontend (optional)**
```bash
cd frontend
npm install
npm run dev
```
- Frontend: http://localhost:5173

### Docker Installation

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access the API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 📖 Usage Guide

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepass123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Available Quests

```bash
curl -X GET "http://localhost:8000/quests/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Submit a Model for Evaluation

Train your model and save it:

```python
from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib

# Load dataset
df = pd.read_csv('datasets/housing_train.csv')
X = df.drop(columns=['price'])
y = df['price']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'my_model.pkl')
```

Submit via API:

```bash
curl -X POST "http://localhost:8000/quests/1/submit" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "model_file=@my_model.pkl"
```

### 5. Check Your Progress

```bash
curl -X GET "http://localhost:8000/user/progress" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. View Leaderboard

```bash
curl -X GET "http://localhost:8000/leaderboard/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🎯 Quest System

### Available Quests

#### Level 1: Regression Basics
- **Quest 1**: Linear Regression Challenge
  - Dataset: Housing prices
  - Metric: R² score
  - Threshold: > 0.80
  - Reward: 100 XP

- **Quest 2**: Advanced Regression
  - Dataset: Housing prices
  - Metric: R² score
  - Threshold: > 0.85
  - Reward: 150 XP

#### Level 2: Classification Mastery
- **Quest 3**: Binary Classification
  - Dataset: Customer churn
  - Metric: Accuracy
  - Threshold: > 0.85
  - Reward: 200 XP

- **Quest 4**: Multi-class Classification
  - Dataset: Iris species
  - Metric: F1-score
  - Threshold: > 0.90
  - Reward: 250 XP

#### Level 3: Advanced ML
- **Quest 5**: Advanced Classification Challenge
  - Dataset: Customer churn
  - Metric: Accuracy
  - Threshold: > 0.90
  - Reward: 300 XP

## 🏆 Badge System

| Badge | Condition | Icon |
|-------|-----------|------|
| First Steps | Complete 1 quest | 🎯 |
| Quest Master | Complete 5 quests | ⭐ |
| XP Hunter | Earn 500 XP | 💎 |
| ML Expert | Earn 1500 XP | 🏆 |
| Streak Champion | 7-day streak | 🔥 |
| Perfectionist | Perfect score on any quest | 💯 |

## 🧪 Testing

### Run Test Suite

```bash
# Make sure server is running
python test_api.py
```

### Run with pytest

```bash
pytest tests/
```

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: JWT secret key (must be 32+ characters)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### Quest Configuration

Quests are configured in `init_db.py`. Each quest has:

- **task_type**: "regression", "classification", "clustering"
- **dataset_name**: CSV file in `datasets/` directory
- **metric_name**: "accuracy", "r2_score", "f1_score", etc.
- **threshold**: Minimum score to pass
- **config**: JSON with dataset-specific settings

Example:
```python
Quest(
    title="Linear Regression Challenge",
    task_type="regression",
    dataset_name="housing_train.csv",
    metric_name="r2_score",
    threshold=0.80,
    config={
        "target_column": "price",
        "test_size": 0.2,
        "random_state": 42
    }
)
```

## 🔌 API Reference

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Quests

- `GET /quests/` - List all quests with completion status
- `GET /quests/{id}` - Get quest details
- `POST /quests/{id}/submit` - Submit model for evaluation
- `GET /quests/{id}/submissions` - Get submission history

### User

- `GET /user/me` - Get current user profile
- `GET /user/progress` - Get detailed progress

### Leaderboard

- `GET /leaderboard/` - Get global rankings

## 🧩 Extending the Platform

### Adding New Quests

1. Add dataset to `datasets/`
2. Update `init_db.py` with new quest configuration
3. Run `python init_db.py` to update database

### Adding New Metrics

Edit `app/ml_engine/evaluator.py` and add to `_calculate_metric()`:

```python
def _calculate_metric(self, y_true, y_pred, metric_name: str) -> float:
    metric_functions = {
        "accuracy": accuracy_score,
        "r2_score": r2_score,
        # Add your custom metric here
        "my_custom_metric": my_custom_function,
    }
    # ...
```

### Adding New Badge Conditions

Edit `app/services/badge_service.py` and add to `_check_badge_condition()`:

```python
def _check_badge_condition(self, user_id: int, badge: Badge) -> bool:
    # Add new condition type
    if badge.condition_type == "my_new_condition":
        # Your logic here
        return True
    # ...
```

## 🔒 Security

- ✅ Passwords hashed with bcrypt
- ✅ JWT token authentication
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ File upload validation

### Production Recommendations

1. Use PostgreSQL instead of SQLite
2. Set strong `SECRET_KEY` (32+ random characters)
3. Enable HTTPS
4. Configure CORS properly
5. Add rate limiting
6. Set up proper logging
7. Use environment-specific configs

## 📊 Database Schema

```sql
users
  - id, username, email, hashed_password
  - xp, level, current_streak, last_activity_date

levels
  - id, name, description, order, required_xp

quests
  - id, level_id, title, description, task_type
  - xp_reward, dataset_name, metric_name, threshold, config

submissions
  - id, user_id, quest_id, model_path
  - score, passed, xp_awarded, evaluation_logs

badges
  - id, name, description, icon
  - condition_type, condition_value

user_badges
  - id, user_id, badge_id, earned_at
```

## 🐛 Troubleshooting

### Database Issues

```bash
# Reset database
rm ml_game_platform.db
python init_db.py
```

### Model Evaluation Fails

- Ensure model is saved in `.pkl` or `.joblib` format
- Check that feature names match dataset
- Verify model is trained on correct dataset

### Authentication Issues

- Check JWT token is included in Authorization header
- Verify token hasn't expired (7 days default)
- Ensure SECRET_KEY is set correctly

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - feel free to use for learning and commercial projects.

## 🙏 Acknowledgments

Built with:
- FastAPI - Modern web framework
- SQLAlchemy - SQL toolkit and ORM
- scikit-learn - Machine learning library
- Pydantic - Data validation

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation at `/docs`
- Review test files for examples

---

**Happy Learning! 🎓🤖**