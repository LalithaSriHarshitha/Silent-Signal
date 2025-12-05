from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import random

from backend.database import get_db
from backend.models import User, Gesture

router = APIRouter()

@router.get("/analytics")
async def get_analytics(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get analytics data for the dashboard
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # For now, return demo data
        # TODO: Replace with actual database queries when gesture logging is implemented
        
        stats = calculate_stats(days, db)
        charts = generate_chart_data(days, db)
        recent_activity = get_recent_activity(db)
        
        return {
            "success": True,
            "stats": stats,
            "charts": charts,
            "recent_activity": recent_activity
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def calculate_stats(days: int, db: Session):
    """Calculate statistics for the dashboard"""
    # TODO: Replace with actual database queries
    
    # Demo data with realistic variations
    base_total = 1000 + random.randint(0, 500)
    base_gestures = base_total * 3 + random.randint(0, 200)
    
    return {
        "total_communications": base_total,
        "total_gestures": base_gestures,
        "avg_confidence": 85 + random.randint(0, 10),
        "active_sessions": random.randint(8, 20),
        "total_change": round(random.uniform(10, 25), 1),
        "gestures_change": round(random.uniform(15, 30), 1),
        "confidence_change": round(random.uniform(2, 8), 1),
        "sessions_change": round(random.uniform(5, 15), 1)
    }

def generate_chart_data(days: int, db: Session):
    """Generate data for all charts"""
    # TODO: Replace with actual database queries
    
    # Activity chart - daily data
    activity_labels = []
    activity_data = []
    for i in range(days - 1, -1, -1):
        date = datetime.now() - timedelta(days=i)
        activity_labels.append(date.strftime("%b %d"))
        activity_data.append(random.randint(20, 80))
    
    # Gesture distribution
    gestures = {
        "labels": ["Hello", "Thank You", "Help", "Yes", "No", "Other"],
        "data": [
            random.randint(300, 500),
            random.randint(250, 400),
            random.randint(150, 250),
            random.randint(200, 350),
            random.randint(100, 200),
            random.randint(150, 300)
        ]
    }
    
    # Confidence distribution
    confidence_data = [
        random.randint(30, 60),    # 0-20%
        random.randint(80, 150),   # 20-40%
        random.randint(200, 350),  # 40-60%
        random.randint(400, 600),  # 60-80%
        random.randint(700, 1000)  # 80-100%
    ]
    
    # Hourly usage
    hourly_data = [
        random.randint(5, 20),    # 12AM
        random.randint(3, 15),    # 3AM
        random.randint(10, 30),   # 6AM
        random.randint(30, 60),   # 9AM
        random.randint(60, 100),  # 12PM
        random.randint(70, 110),  # 3PM
        random.randint(50, 80),   # 6PM
        random.randint(25, 50)    # 9PM
    ]
    
    return {
        "activity": {
            "labels": activity_labels,
            "data": activity_data
        },
        "gestures": gestures,
        "confidence": {
            "data": confidence_data
        },
        "hourly": {
            "data": hourly_data
        }
    }

def get_recent_activity(db: Session, limit: int = 10):
    """Get recent activity for the table"""
    # TODO: Replace with actual database queries
    
    gestures = ["Hello", "Thank You", "Help", "Yes", "No", "Please"]
    outputs = [
        "Hello, how are you?",
        "Thank you very much",
        "I need help",
        "Yes, I agree",
        "No, thank you",
        "Please help me"
    ]
    
    activities = []
    for i in range(limit):
        minutes_ago = i * 3 + random.randint(1, 5)
        gesture_idx = random.randint(0, len(gestures) - 1)
        
        activities.append({
            "time": f"{minutes_ago} mins ago" if minutes_ago < 60 else f"{minutes_ago // 60} hours ago",
            "type": "Gesture",
            "gesture": gestures[gesture_idx],
            "confidence": random.randint(70, 98),
            "output": outputs[gesture_idx],
            "status": "Success"
        })
    
    return activities
