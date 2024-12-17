# Compendium

This project uses Claude AI to extract key points and summarize articles based on user input. It gathers relevant keywords and then provides recent articles (within the past month) and research papers (from any time) based on the extracted keywords.
Created by Elias, Guanyi, Ethan, and Jacob

## Demo
https://youtu.be/SVOS7w1R5TE

## Features

- **Input Handling**: Take user input in the form of text or URL and process it using Claude AI.
- **Key Point Extraction**: Claude AI identifies and extracts the key points from the provided content.
- **Summarization**: Provides a concise summary of the article or research paper.
- **Keyword Generation**: Extracts important keywords from the input for more relevant search results.
- **Recent Articles Retrieval**: Searches for and retrieves articles published within the past month that match the extracted keywords.
- **Research Papers Search**: Retrieves research papers (from any time) based on the generated keywords.

## Setup Instructions

1. **Create a New Folder:**
   Create a new folder named `anything_you_want`.

   ```bash
   mkdir anything_you_want
   cd anything_you_want
   ```

2. **Create a Virtual Environment:**
   Run the following command to create a virtual environment inside the folder:

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   Activate the virtual environment and move into it:

   ```bash
   source ./venv/bin/activate
   cd venv
   ```

4. **Install Dependencies:**
   - Move the `requirements.txt` file from our `venv` folder into your `venv` folder.
   - Run the following command to install the dependencies listed in the `requirements.txt` file:

   ```bash
   pip3 install -r requirements.txt
   ```

5. **Create Configuration Files:**
   - Create a `.env` file and `.gitignore` file in the `venv` folder.
   - The .gitignore should say
      ```
      venv
      INRIX-Access
      ```

6. **Set Up AWS Credentials:**
   The `.env` file should contain your AWS credentials in the following format:

   ```
   AWS_ACCESS_KEY_ID="your-access-key-id"
   AWS_SECRET_ACCESS_KEY="your-secret-access-key"
   ```

   To get your AWS credentials, follow these steps:
   1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
   2. Navigate to the **IAM (Identity and Access Management)** dashboard.
   3. Select **Users** from the sidebar and click on your user name.
   4. Go to the **Security credentials** tab and click **Create access key**.
   5. Download or copy the `Access Key ID` and `Secret Access Key`.

   After obtaining your credentials, add them to the `.env` file as shown above.

7. **Install NewsAPI Python Client:**
   Run the following command to install the `newsapi-python` package:

   ```bash
   pip3 install newsapi-python
   ```

8. **Install Flask:**
   Run the following command to install `Flask`:

   ```bash
   pip3 install Flask
   ```
   
9. **Move Project Files:**
   - Move our `static` folder, `templates` folder, and `converse.py` file into your `venv` folder.

10. **Run the Application:**
   Run the `converse.py` script using the following command:

   ```bash
   python3 converse.py
   ```
