# Curriculum Compass

An intelligent web scraper that extracts course prerequisites from MIT OpenCourseWare (OCW) syllabi and converts them into structured JSON data. Uses AI-powered text parsing and comprehensive course code mapping for accurate, human-readable results.

## Features

- **Smart Web Scraping**: Extracts prerequisite information from MIT OCW syllabus pages using BeautifulSoup
- **AI-Powered Parsing**: Leverages Groq's LLaMA 3.1 model to intelligently parse unstructured prerequisite text
- **Course Code Mapping**: Automatically maps MIT course codes (e.g., `6.001`, `18.02`) to full course names using a comprehensive CSV database
- **50+ Courses Available**: Pre-configured with 50 popular MIT courses across multiple departments
- **Interactive CLI**: User-friendly command-line interface for course selection
- **JSON Output**: Clean, structured output format perfect for further processing

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key 

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd curriculum-compass
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   **Tip**: Use `env_template.txt` as a reference for the required format.

4. **Run the scraper**
   ```bash
   python course_curriculum.py
   ```

## How It Works

### The Scraping Process

1. **Course Selection**: Choose from 50 curated MIT courses spanning:
   - Mathematics (Calculus, Linear Algebra, Differential Equations)
   - Computer Science (Algorithms, AI/ML, Systems Programming)
   - Physics & Engineering (Quantum Physics, Materials Science)
   - And more!

2. **Web Scraping**: The scraper navigates to the course's MIT OCW syllabus page and intelligently extracts prerequisite sections using regex patterns and DOM parsing.

3. **AI Processing**: Raw prerequisite text is sent to Groq's LLaMA 3.1 model with specialized prompts to:
   - Identify course codes vs. general requirements
   - Structure information into JSON format
   - Handle edge cases and ambiguous text

4. **Course Mapping**: Extracted course codes are mapped to full course names using the comprehensive `COURSE CODES.csv` database (665+ MIT courses).

5. **Output Generation**: Returns clean JSON with the course name and a list of human-readable prerequisites.

## Example Usage

```bash
$ python course_curriculum.py

MIT OCW Prerequisite Scraper
========================================

Available courses:
 1. 18.01SC Single Variable Calculus
 2. 18.02SC Multivariable Calculus
 ...
26. 6.034 Artificial Intelligence
 ...

Enter the course number you want to scrape (1-50): 26

Scraping prerequisites for: 6.034 Artificial Intelligence
==================================================
Raw prerequisite text: 6.001: We will have regular assignments that expect you to be able to read and write Scheme. This is the only formal pre-requisite. 18.02: We will assume that you know what the chain rule is...

==================================================
RESULT:
{
    "course": "6.034 Artificial Intelligence",
    "prerequisites": [
        "Structure and Interpretation of Computer Programs",
        "Multivariable Calculus"
    ]
}
```

## Architecture

### Core Components

- **`get_course_data()`**: Maintains the curated list of 50 MIT courses with their OCW URLs
- **`scrape_prerequisites(url)`**: Handles web scraping with robust error handling and multiple parsing strategies
- **`extract_prereqs(course_name, text)`**: Interfaces with Groq's LLaMA model for AI-powered text parsing
- **`map_course_code_to_name(code)`**: Maps MIT course codes to full names using the CSV database

### Data Flow

```
User Input → Course Selection → Web Scraping → AI Parsing → Course Mapping → JSON Output
```

## Project Structure

```
curriculum-compass/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── .env                   # API key (create this)
├── course_curriculum.py   # Main scraper application
├── COURSE CODES.csv       # Course code → name mappings (665 courses)
├── env_template.txt       # Environment template
└── .gitignore            # Git ignore rules
```

## Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `requests` | HTTP requests for web scraping | ≥2.31.0 |
| `beautifulsoup4` | HTML parsing | ≥4.12.0 |
| `pandas` | CSV data processing | ≥2.0.0 |
| `groq` | AI model API client | ≥0.4.0 |
| `python-dotenv` | Environment variable management | ≥1.0.0 |
| `lxml` | XML/HTML parser backend | ≥4.9.0 |

## Available Course Categories

### Mathematics (8 courses)
- Single/Multivariable Calculus
- Linear Algebra variants
- Differential Equations
- Probability & Statistics

### Computer Science (20 courses)
- Programming foundations (Python, C++)
- Algorithms & Data Structures
- AI/Machine Learning (6 courses)
- Systems (Networks, Databases, OS)

### Physics & Engineering (22 courses)
- Classical/Quantum Physics
- Materials Science
- Mechanical Engineering
- Control Systems

## Configuration

### Course Database
The `COURSE CODES.csv` file contains 665+ MIT course mappings in the format:
```csv
Course ID,Course Name
6.001,Structure and Interpretation of Computer Programs
18.02,Multivariable Calculus
...
```

### Adding New Courses
To add courses to the scraper, edit the `get_course_data()` function in `course_curriculum.py`:

```python
{"id": 51, "title": "New Course Title", "url": "https://ocw.mit.edu/courses/..."}
```

## Error Handling

The scraper includes robust error handling for:
- **Network issues**: Timeout handling and connection errors
- **Missing prerequisites**: Graceful handling when no prerequisites are found
- **AI parsing failures**: Fallback to empty prerequisites list
- **Invalid course codes**: Unmapped codes are returned as-is

## Contributing

Contributions are welcome! Areas for improvement:
- Additional MIT courses
- Enhanced prerequisite detection algorithms
- Support for other universities
- Web interface development

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues:
1. Ensure your Groq API key is valid and has sufficient credits
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check that `COURSE CODES.csv` is in the same directory
4. Review the console output for specific error messages

---

*Built for the MIT academic community and beyond.*