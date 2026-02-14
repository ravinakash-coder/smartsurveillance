# Contributing to SmartSurveillance

Thank you for considering contributing to SmartSurveillance! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Be patient with new contributors
- Focus on the code, not the person

## How to Contribute

### 1. Reporting Bugs

**Before submitting a bug report:**
- Check if the issue already exists
- Update to the latest version
- Collect relevant information:
  - OS and Python version
  - Steps to reproduce
  - Expected vs actual behavior
  - Error logs/screenshots

**Submit via GitHub Issues with:**
- Clear descriptive title
- Detailed description
- Code snippets/logs if applicable
- System information

### 2. Suggesting Features

**Before suggesting a feature:**
- Check if it's already proposed
- Make sure it aligns with project goals

**Provide:**
- Clear use case
- Potential implementation approach
- Benefits to users

### 3. Code Contributions

#### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/SmartSurveillance.git
cd SmartSurveillance

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Install dev dependencies
pip install -r requirements-dev.txt
```

#### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow PEP 8 style guide
   - Add type hints
   - Write docstrings
   - Keep commits atomic

3. **Write tests:**
   ```bash
   # Add tests for new features in tests/
   pytest tests/
   ```

4. **Format code:**
   ```bash
   black src/ tests/
   isort src/ tests/
   ```

5. **Check code quality:**
   ```bash
   flake8 src/ tests/
   mypy src/
   ```

6. **Run full test suite:**
   ```bash
   pytest --cov=src tests/
   ```

#### Code Standards

**Python Style:**
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters (except URLs)
- Use meaningful variable names

**Type Hints:**
```python
from typing import List, Optional, Tuple
import numpy as np

def process_frame(frame: np.ndarray, 
                 confidence: float = 0.5) -> Optional[List[dict]]:
    """
    Process a frame with detection.
    
    Args:
        frame: Input image array
        confidence: Confidence threshold
        
    Returns:
        List of detections or None
    """
    pass
```

**Docstrings:**
```python
def detect_objects(frame: np.ndarray) -> List[Detection]:
    """
    Detect objects in frame using YOLOv8.
    
    Performs real-time object detection using the YOLOv8 model.
    Filters results by confidence threshold and target classes.
    
    Args:
        frame: Input image frame as numpy array
        
    Returns:
        List of Detection objects with class info and bounding boxes
        
    Raises:
        ValueError: If frame is invalid
        RuntimeError: If model fails to process
        
    Example:
        >>> frame = cv2.imread('image.jpg')
        >>> detections = detect_objects(frame)
        >>> for det in detections:
        ...     print(f"{det.class_name}: {det.confidence:.2%}")
    """
    pass
```

### 4. Documentation

**Improve documentation by:**
- Fixing typos
- Clarifying explanations
- Adding examples
- Updating outdated information

**Edit these files:**
- `README.md` - Main documentation
- `GETTING_STARTED.md` - Setup guide
- Docstrings in code - API documentation

### 5. Pull Request Process

1. **Create Pull Request:**
   - Reference any related issues (Fixes #123)
   - Provide clear description of changes
   - Include motivation and context

2. **PR Title Format:**
   ```
   [TYPE] Short description
   
   Types: feat, fix, refactor, docs, test, chore
   Examples:
   - feat: Add motion detection algorithm
   - fix: Handle empty frames gracefully
   - docs: Update installation guide
   ```

3. **PR Description Template:**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Related Issues
   Closes #123
   
   ## Testing
   - [ ] Unit tests added
   - [ ] Manual testing done
   - [ ] No new warnings
   
   ## Checklist
   - [ ] Code follows style guide
   - [ ] Comments added where needed
   - [ ] Documentation updated
   - [ ] Tests pass locally
   ```

4. **Code Review:**
   - Address feedback promptly
   - Don't dismiss suggestions without discussion
   - Push new commits to update PR (don't force push)

## Development Areas

### High Priority
- Performance optimization
- GPU acceleration support
- Additional alert mechanisms (SMS, webhooks)
- Web dashboard
- Mobile app

### Medium Priority
- Recording capabilities
- Multi-camera support
- Advanced analytics
- API development
- Database integration

### Nice to Have
- Facial recognition
- Behavior analysis
- 3D visualization
- Cloud integration
- Machine learning model optimization

## Project Structure

```
SmartSurveillance/
├── src/
│   ├── frame_grabber.py      # Video capture
│   ├── object_detector.py    # YOLOv8 detection
│   ├── alert_system.py       # Alerts/notifications
│   ├── orchestrator.py       # Component coordination
│   ├── config.py             # Configuration
│   ├── gui.py                # PyQt5 interface
│   └── utils.py              # Utility functions
├── tests/
│   └── test_components.py    # Unit tests
├── Doc/
│   └── ProjectSSummary.md    # Project overview
└── [config and doc files]
```

### Module Responsibilities

- **frame_grabber.py**: Video source handling
- **object_detector.py**: YOLOv8 integration
- **alert_system.py**: Email and notifications
- **orchestrator.py**: System coordination
- **config.py**: Configuration management
- **gui.py**: User interface
- **utils.py**: Common utilities

## Testing Guidelines

```python
# tests/test_components.py

class TestMyFeature(unittest.TestCase):
    """Test description"""
    
    def setUp(self):
        """Setup test fixtures"""
        pass
    
    def test_something(self):
        """Test case description"""
        self.assertEqual(expected, actual)
    
    def tearDown(self):
        """Cleanup"""
        pass
```

**Run tests:**
```bash
pytest tests/                    # Run all tests
pytest tests/test_file.py        # Run specific file
pytest tests/ -v                 # Verbose output
pytest --cov=src tests/          # With coverage
```

## Commit Guidelines

- **Atomic commits**: One logical change per commit
- **Clear messages**: Describe what and why, not how
- **Reference issues**: "Fixes #123, Closes #456"

**Format:**
```
[TYPE] Short description (50 chars max)

Detailed explanation of changes if needed.
Can span multiple lines.

- Bullet points for multiple changes
- Another point

Fixes #123
```

**Examples:**
```
fix: Handle None frames in detector

feat: Add motion detection threshold

docs: Update Gmail setup instructions

test: Add frame grabber unit tests

refactor: Simplify alert logic
```

## Questions?

- Create an issue with your question
- Check existing documentation
- Review code comments and docstrings
- Ask in discussions section

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for major contributions
- GitHub contributors page

Thank you for contributing to SmartSurveillance! 🎉
