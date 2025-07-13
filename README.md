# TrackLeh - Smart Expense Tracker

A modern expense tracking application designed to eliminate the manual entry overhead and forgetfulness that plague traditional expense trackers. Built for busy users who want proactive financial management without the hassle.

## 🎯 Project Motivation

TrackLeh was created to solve common pain points with existing expense tracker apps:
- **Manual entry overhead** - Tedious data input that users often skip
- **Forgetfulness** - Leading to inconsistent and inaccurate tracking
- **Poor user experience** - Apps that feel like work rather than helpful tools

The app targets users who may be busy or "lazy" but want to proactively manage their finances with minimal effort.

## ✨ Features

### Current MVP Features
- Basic expense entry and tracking
- Simple categorization system
- Essential data visualization
- User-friendly interface

### Planned Advanced Features
- **NLP-powered automatic entry logging** - Smart text parsing for effortless expense entry
- **AI-powered smart categorization** - Automatic expense categorization based on patterns
- **Smart nudges** - Behavior-based, non-annoying notifications to encourage consistent tracking
- **OCR for receipt scanning** - Automatic entry logging from photos of receipts and documents
- **Customizable expense categories** - Flexible categorization system tailored to user needs
- **Comprehensive analytics** - Advanced data visualization and insights
- **Anomaly detection** - AI-powered suggestions and unusual spending alerts

*Note: Advanced features may evolve based on user feedback and testing.*

## 🛠️ Tech Stack

### MVP Stack
- **Frontend**: React Native - Cross-platform mobile development
- **Backend**: FastAPI - Modern, fast web framework for building APIs
- **Database**: PostgreSQL - Robust relational database
- **Database Migration**: Alembic - Database schema version control
- **ORM**: SQLAlchemy - Python SQL toolkit and Object-Relational Mapping
- **Testing**: Pytest - Python testing framework

### Future Considerations
The tech stack may evolve as the project grows and requirements become clearer through user feedback and development experience.

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- PostgreSQL
- React Native development environment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/timhye/trackleh.git
   cd trackleh
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Set up database
   alembic upgrade head
   
   # Start the server
   uvicorn backend.main:app --reload
   ```

3. **Frontend Setup(Not Yet Implemented)**
   ```bash
   cd frontend
   npm install
   
   # For iOS
   npx react-native run-ios
   
   # For Android
   npx react-native run-android
   ```

## 🧪 Testing

Run the test suite:
```bash
cd backend
pytest
```

## 📱 Current Goal

Build an MVP to deliver basic functionality while learning best practices for:
- Development workflows
- Testing strategies
- Deployment processes
- User feedback collection

## 🤝 Contributing

This project is currently in MVP development phase. Contributions, suggestions, and feedback are welcome!
