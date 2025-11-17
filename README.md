# Real Estate Analysis Chatbot 🏠

A full-stack web application that provides AI-powered analysis of real estate data through an interactive chatbot interface. Built with React and Django, this application allows users to query property trends, compare localities, and visualize market data.

![Real Estate Chatbot](https://img.shields.io/badge/React-18.2.0-blue) ![Django](https://img.shields.io/badge/Django-4.2.7-green) ![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## 🎯 Features

### Core Features

- ✅ **Interactive Chat Interface** - Natural language query processing for real estate analysis
- ✅ **Excel Data Processing** - Upload and analyze real estate datasets from Excel files
- ✅ **Data Visualization** - Dynamic charts showing price trends, demand patterns, and comparisons
- ✅ **Filtered Data Tables** - View detailed property data with inline filtering
- ✅ **Smart Query Parsing** - Automatically detects localities and analysis intent from user queries

### Bonus Features

- 🎁 **Data Export** - Download filtered data as CSV files
- 🎁 **OpenAI Integration** - Optional LLM integration for real AI-generated summaries
- 🎁 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🎁 **Multiple Comparison** - Compare demand and price trends across multiple localities

## 🛠️ Tech Stack

### Frontend

- **React 18.2** - UI framework
- **React Bootstrap** - UI components
- **Chart.js** with react-chartjs-2 - Data visualization
- **Axios** - API communication
- **Bootstrap 5** - Styling

### Backend

- **Django 4.2** - Web framework
- **Django REST Framework** - API endpoints
- **Pandas** - Data processing
- **openpyxl** - Excel file handling
- **CORS Headers** - Cross-origin support

## 📋 Prerequisites

- **Node.js** 16+ and npm
- **Python** 3.8+
- **pip** (Python package manager)

## 🚀 Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**

```bash
cd backend
```

2. **Create and activate virtual environment:**

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env and add your configuration
```

5. **Run migrations:**

```bash
python manage.py migrate
```

6. **Create superuser (optional):**

```bash
python manage.py createsuperuser
```

7. **Start the development server:**

```bash
python manage.py runserver
```

The backend will be running at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
```

3. **Set up environment variables:**

```bash
cp .env.example .env
# The default API URL is http://localhost:8000/api
```

4. **Start the development server:**

```bash
npm start
```

The frontend will be running at `http://localhost:3000`

## 📊 Sample Data

You can use the provided sample Excel file from the assignment:
[Download Sample Data](https://docs.google.com/spreadsheets/d/1BPFvRBLAFFLyQ1EDJ4ogXt8HYCUXhM80/edit?usp=sharing&ouid=106548111997272759849&rtpof=true&sd=true)

The Excel file should contain columns like:

- **Year** - Year of the record
- **Area/Locality** - Name of the locality
- **Price** - Average property price
- **Demand** - Number of transactions/demand metric
- **Size** - Property size in square feet (optional)

## 💡 Usage

### Uploading Data

1. Click on the file upload button in the sidebar
2. Select your Excel file (.xlsx or .xls)
3. Wait for the upload confirmation

### Querying Data

Type natural language queries in the chat input. Examples:

- **"Analyze Wakad"** - Get comprehensive analysis of Wakad area
- **"Compare Ambegaon Budruk and Aundh demand trends"** - Compare two localities
- **"Show price growth for Akurdi over the last 3 years"** - View price trends
- **"Give me analysis of Kharadi"** - General area analysis

### Understanding Responses

Each query returns:

1. **Text Summary** - Natural language analysis of the data
2. **Chart** - Visual representation (line charts for trends)
3. **Data Table** - Filtered records with download option

### Downloading Data

Click the "Download CSV" button on any data table to export the filtered results.

## 🔧 API Endpoints

### POST `/api/upload/`

Upload Excel file for analysis

- **Body:** `multipart/form-data` with file
- **Response:** File path and available areas

### POST `/api/query/`

Process natural language query

- **Body:** `{ "query": "string", "file_path": "string" }`
- **Response:** Summary, chart data, and table data

### GET `/api/areas/`

Get list of available areas

- **Query Params:** `file_path` (optional)
- **Response:** Array of area names

### POST `/api/export/`

Export filtered data

- **Body:** `{ "area": "string", "file_path": "string" }`
- **Response:** Filtered data array

## 🎨 Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   React Frontend│◄────────┤  Django Backend │
│   (Port 3000)   │  REST   │   (Port 8000)   │
└─────────────────┘   API   └─────────────────┘
         │                            │
         │                            │
    ┌────▼────┐                 ┌────▼────┐
    │ Chart.js │                 │  Pandas │
    │ Bootstrap│                 │ openpyxl│
    └─────────┘                 └─────────┘
```

## 🔐 Environment Variables

### Backend (.env)

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-key (optional)
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🌐 Deployment

### Backend Deployment (Render/Heroku)

1. **Prepare for deployment:**

```bash
pip freeze > requirements.txt
```

2. **Add Procfile:**

```
web: gunicorn realestate_chatbot.wsgi
```

3. **Install gunicorn:**

```bash
pip install gunicorn
```

4. **Update settings.py:**

```python
ALLOWED_HOSTS = ['your-domain.com', 'localhost']
DEBUG = False
```

### Frontend Deployment (Vercel/Netlify)

1. **Build the application:**

```bash
npm run build
```

2. **Update environment variables** on your hosting platform with production API URL

3. **Deploy the build folder**

## 📹 Demo Video

[Record a 1-2 minute demo video showing:]

1. Uploading an Excel file
2. Running different types of queries
3. Viewing charts and data tables
4. Downloading data
5. Comparing multiple localities

## 🧪 Testing

### Backend Tests

```bash
cd backend
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📝 Project Structure

```
SigmaValue/
├── backend/
│   ├── realestate_chatbot/     # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/                    # API app
│   │   ├── views.py           # API endpoints
│   │   ├── urls.py            # URL routing
│   │   ├── data_processor.py  # Excel processing logic
│   │   └── llm_integration.py # Optional OpenAI integration
│   ├── data/                   # Data storage
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Message.js
│   │   │   ├── ChartComponent.js
│   │   │   └── DataTable.js
│   │   ├── services/          # API services
│   │   │   └── api.js
│   │   ├── App.js             # Main application
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
│
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

**1. CORS Errors**

- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOW_ALL_ORIGINS = True` in settings.py

**2. File Upload Fails**

- Verify Excel file format (.xlsx or .xls)
- Check file size limits
- Ensure `media` folder has write permissions

**3. Chart Not Displaying**

- Verify data structure has `labels` and `datasets`
- Check browser console for errors
- Ensure Chart.js is properly installed

**4. Query Returns No Results**

- Verify area name matches exactly with data
- Check Excel column names (Area, Year, Price, Demand)
- Try uploading a new file

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of the SigmaValue Full Stack Developer Assignment.

## 👨‍💻 Author

**[Your Name]**

- GitHub: [@yourusername]
- Email: your.email@example.com

## 🙏 Acknowledgments

- SigmaValue for the assignment opportunity
- React and Django communities for excellent documentation
- Chart.js for powerful visualization capabilities

## 📞 Support

For questions or issues, please:

1. Check the troubleshooting section
2. Open an issue on GitHub
3. Contact via email

---

**Built with ❤️ for SigmaValue Assignment**
