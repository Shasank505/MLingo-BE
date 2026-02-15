"""
Initialize database with sample levels, quests, and badges
"""
from app.database import SessionLocal, init_db
from app.models import Level, Quest, Badge


def seed_database():
    """Seed database with initial data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Level).first():
            print("Database already seeded")
            return
        
        # Create Levels
        level1 = Level(
            name="Regression Basics",
            description="Learn the fundamentals of regression analysis",
            order=1,
            required_xp=0
        )
        
        level2 = Level(
            name="Classification Mastery",
            description="Master classification algorithms",
            order=2,
            required_xp=500
        )
        
        level3 = Level(
            name="Advanced ML",
            description="Advanced machine learning techniques",
            order=3,
            required_xp=1500
        )
        
        db.add_all([level1, level2, level3])
        db.commit()
        
        # Create Quests for Level 1
        quest1 = Quest(
            level_id=level1.id,
            title="Linear Regression Challenge",
            description="Build a linear regression model to predict housing prices. Achieve R² score > 0.8",
            task_type="regression",
            order=1,
            xp_reward=100,
            dataset_name="housing_train.csv",
            metric_name="r2_score",
            threshold=0.80,
            config={
                "target_column": "price",
                "test_size": 0.2,
                "random_state": 42
            }
        )
        
        quest2 = Quest(
            level_id=level1.id,
            title="Advanced Regression",
            description="Improve your model! Achieve R² score > 0.85",
            task_type="regression",
            order=2,
            xp_reward=150,
            dataset_name="housing_train.csv",
            metric_name="r2_score",
            threshold=0.85,
            config={
                "target_column": "price",
                "test_size": 0.2,
                "random_state": 42
            }
        )
        
        # Create Quests for Level 2
        quest3 = Quest(
            level_id=level2.id,
            title="Binary Classification",
            description="Build a classifier to predict customer churn. Achieve accuracy > 85%",
            task_type="classification",
            order=1,
            xp_reward=200,
            dataset_name="churn_train.csv",
            metric_name="accuracy",
            threshold=0.85,
            config={
                "target_column": "churn",
                "test_size": 0.2,
                "random_state": 42
            }
        )
        
        quest4 = Quest(
            level_id=level2.id,
            title="Multi-class Classification",
            description="Classify iris species with F1-score > 0.90",
            task_type="classification",
            order=2,
            xp_reward=250,
            dataset_name="iris_train.csv",
            metric_name="f1_score",
            threshold=0.90,
            config={
                "target_column": "species",
                "test_size": 0.2,
                "random_state": 42
            }
        )
        
        # Create Quests for Level 3
        quest5 = Quest(
            level_id=level3.id,
            title="Advanced Classification Challenge",
            description="Build a high-performance classifier. Achieve accuracy > 90%",
            task_type="classification",
            order=1,
            xp_reward=300,
            dataset_name="churn_train.csv",
            metric_name="accuracy",
            threshold=0.90,
            config={
                "target_column": "churn",
                "test_size": 0.2,
                "random_state": 42
            }
        )
        
        db.add_all([quest1, quest2, quest3, quest4, quest5])
        db.commit()
        
        # Create Badges
        badges = [
            Badge(
                name="First Steps",
                description="Complete your first quest",
                icon="🎯",
                condition_type="quest_completion",
                condition_value=1
            ),
            Badge(
                name="Quest Master",
                description="Complete 5 quests",
                icon="⭐",
                condition_type="quest_completion",
                condition_value=5
            ),
            Badge(
                name="XP Hunter",
                description="Earn 500 XP",
                icon="💎",
                condition_type="xp_threshold",
                condition_value=500
            ),
            Badge(
                name="ML Expert",
                description="Earn 1500 XP",
                icon="🏆",
                condition_type="xp_threshold",
                condition_value=1500
            ),
            Badge(
                name="Streak Champion",
                description="Maintain a 7-day streak",
                icon="🔥",
                condition_type="streak",
                condition_value=7
            ),
            Badge(
                name="Perfectionist",
                description="Achieve a perfect score on any quest",
                icon="💯",
                condition_type="perfect_score",
                condition_value=1
            ),
        ]
        
        db.add_all(badges)
        db.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   - Created {db.query(Level).count()} levels")
        print(f"   - Created {db.query(Quest).count()} quests")
        print(f"   - Created {db.query(Badge).count()} badges")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding database...")
    seed_database()