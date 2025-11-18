# Django Quiz & Event App

A modern web application built with Django for creating and taking quizzes, as well as managing events. The application features a clean, responsive UI powered by TailwindCSS.

## Features

### Quiz Section
- **List all available quizzes** - Browse through all available quizzes
- **Start a quiz** - Users can select and start any quiz
- **Dynamic question loading** - Questions and answers are loaded dynamically via AJAX
- **Real-time scoring** - Automatic score calculation upon submission
- **Result display** - Detailed results page showing correct/incorrect answers
- **Submission tracking** - All quiz submissions are saved with user names and scores
- **Quiz history** - View all past quiz submissions with detailed statistics

### Event Section
- **Upcoming events display** - View all upcoming events with title, date, and location
- **Event filtering** - Only shows events with future dates

### Frontend
- **Modern UI** - Built with TailwindCSS for a beautiful, responsive design
- **Responsive layout** - Works seamlessly on desktop, tablet, and mobile devices
- **User-friendly navigation** - Easy-to-use navigation bar with all main sections

## Technologies Used

- **Backend**: Django 5.2.8
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML5, JavaScript (Vanilla JS)
- **Styling**: TailwindCSS (via CDN)
- **Python**: 3.x

## Project Structure

```
DJnago_Quiz_Event_App/
├── manage.py
├── db.sqlite3
├── DJnago_Quiz_Event_App/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── quizzes/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    ├── migrations/
    │   └── 0001_initial.py
    └── templates/
        └── quizzes/
            ├── base.html
            ├── home.html
            ├── quiz_list.html
            ├── quiz_attempt.html
            ├── quiz_result.html
            ├── quiz_history.html
            └── events.html
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd DJango/DJnago_Quiz_Event_App
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install django
```

Or if you have a requirements.txt file:

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

To access the Django admin panel for managing quizzes and events:

```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Accessing the Application

1. **Home Page** (`/`): View latest quizzes and upcoming events
2. **Quiz List** (`/quizzes/`): Browse all available quizzes
3. **Take Quiz** (`/quizzes/<id>/`): Start a quiz attempt
4. **Quiz Results** (`/results/<submission_id>/`): View detailed quiz results
5. **Quiz History** (`/history/`): View all quiz submissions
6. **Events** (`/events/`): View upcoming events

### Managing Quizzes and Events

Use the Django admin panel at `/admin/` to:
- Create, edit, and delete quizzes
- Add questions to quizzes
- Add answers to questions (mark correct answers)
- Create and manage events

### Admin Panel Features

The admin panel includes:
- **Quiz Management**: Full CRUD operations for quizzes
- **Question Management**: Add multiple questions per quiz
- **Answer Management**: Add multiple answers per question with correct answer marking
- **Submission Viewing**: View all user submissions
- **Event Management**: Create and manage events

## Database Models

### Quiz
- `id`: Primary key
- `title`: Quiz title
- `description`: Quiz description
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Question
- `id`: Primary key
- `quiz`: Foreign key to Quiz
- `text`: Question text
- `question_type`: Type of question (multiple_choice, single_choice, text)
- `created_at`: Creation timestamp

### Answer
- `id`: Primary key
- `question`: Foreign key to Question
- `text`: Answer text
- `is_correct`: Boolean indicating if answer is correct

### UserSubmission
- `id`: Primary key
- `quiz`: Foreign key to Quiz
- `user_name`: Name of the user taking the quiz
- `score`: Number of correct answers
- `submitted_at`: Submission timestamp

### UserAnswer
- `id`: Primary key
- `submission`: Foreign key to UserSubmission
- `question`: Foreign key to Question
- `answer`: Foreign key to Answer
- `is_correct`: Boolean indicating if the answer was correct
- **Constraint**: Unique constraint on (submission, question) to prevent duplicate answers

### Event
- `id`: Primary key
- `title`: Event title
- `description`: Event description
- `date`: Event date
- `location`: Event location

## API Endpoints

### JSON Endpoints

- `GET /quizzes/<id>/data/`: Returns quiz data with questions and answers in JSON format
- `POST /quizzes/<id>/submit/`: Submits quiz answers and returns score

### Request Format for Quiz Submission

```json
{
  "user_name": "John Doe",
  "answers": {
    "1": "3",
    "2": "5",
    "3": "8"
  }
}
```

Where keys are question IDs and values are answer IDs.

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

## Configuration

### Database Configuration

By default, the application uses SQLite. To use PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Security Settings

Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Set up proper static file serving
5. Use a production database (PostgreSQL recommended)
6. Enable HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Developed as a Django learning project.

## Acknowledgments

- Django framework for the robust backend
- TailwindCSS for the beautiful UI components
- All contributors and users of this application

---

**Note**: This is a development project. For production use, ensure proper security measures, database optimization, and deployment configurations are in place.
