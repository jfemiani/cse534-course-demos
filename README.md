# CSE 534 Course Demos

This repository contains the **Python demonstrations** used in CSE 534: Generative Artificial Intelligence at Miami University.

## Repository Organization

### Demos
Each module contains numbered Python demos that are **linked from Canvas pages**. This is the only robust way to embed code in Canvas at Miami.

**Demo naming convention**: `modulename/01_something.py`

Each demo folder contains:
- The reviewed Python file used in the course
- A `PROMPT.md` file that can regenerate the example or ask an AI assistant to explain it

### Pages and Slides
Course content (pages and slides) are organized alongside the demos:

- **Pages**: `modulename/pages/1. Some Topic.html` (HTML exported from Canvas)
- **Slides**: `modulename/pages/1. Some Topic Slides.tex` and `.pdf` (LaTeX source and built PDF)

Both pages and slides use the **same numbering and naming** to maintain consistency with Canvas.

## Course Modules

### 1. Introduction to Generative AI and its Applications
_(Canvas only - no local demos)_

### 2. [Prompt Engineering and API Integration](02_prompt_engineering_api)
Six introductory demonstrations covering API requests, chat, streaming, Rich terminal formatting, and structured output.

**Demos**:
- `01_hello/` - First API request
- `02_chat/` - Non-streaming chat
- `03_chat_streaming/` - Streaming chat responses
- `04_rich_basics/` - Rich terminal formatting
- `05_rich_chat/` - Rich-formatted chat
- `06_structured_output/` - Structured JSON responses

### 3. [Mathematical Foundations](03_mathematical_foundations)
Probability, entropy, language models, and statistical foundations for AI.

**Demos**:
- `01_uniform/` - Continuous uniform distribution
- `02_bernoulli/` - Bernoulli distribution
- `03_categorical/` - Categorical distribution  
- `04_joint_conditional/` - Joint and conditional probability
- `05_likelihood/` - Likelihood and MLE
- `06_entropy/` - Entropy and information theory
- `07_ngram/` - N-gram language models
- `08_normal/` - Normal distributions
- `09_gaussian_regression/` - Gaussian regression
- `10_multivariate/` - Multivariate normal distributions
- `11_transform/` - Distribution transformations
- `12_mahalanobis/` - Mahalanobis distance
- `13_eigenfaces/` - PCA and eigenfaces

**Pages**: 8 HTML pages covering probability through multivariate statistics (see `pages/` folder)

**Slides**: LaTeX slides available for select topics

## Running a Demonstration

1. Navigate to the relevant module folder
2. Read the module's README and the corresponding Canvas lesson
3. Install requirements: `pip install -r requirements-[module].txt`
4. Run the demo: `python 01_something.py`

## Development Notes

- Canvas pages are the source of truth for course content
- HTML pages are exported from Canvas and stored locally for reference
- Slides are created in LaTeX and both `.tex` source and `.pdf` builds are committed
- Demos are referenced from Canvas pages and course videos
