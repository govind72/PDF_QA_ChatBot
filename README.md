# PDF Q&A ChatBot

This project allows users to upload a PDF document and ask questions based on its content. The chatbot uses OpenAI's API to process and respond to user queries about the PDF.

## Setup

### Step 1: Copy the Environment Example File

First, copy the example environment file to create your own `.env` file:

```bash
cp .env.example .env
```
### Step 2: Add Your OpenAI API Key

OPENAI_API_KEY=your_openai_api_key_here

### Step 3: Create a Virtual Environment

```bash
python -m venv myenv
```
### Step 4: Activate the Virtual Environment

```bash
source myenv/bin/activate
```
### Step 5: Install the Required Packages
```bash
pip install -r requirements.txt
```
### Step 6: Run the Application

```bash
chainlit run app.py -w
````
