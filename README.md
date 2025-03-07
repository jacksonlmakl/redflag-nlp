# RedFlag-NLP

RedFlag-NLP is an AI-powered natural language processing (NLP) agent designed to analyze and flag potentially problematic text content. It leverages OpenAI's GPT models to provide contextual analysis and classification of textual data.

## Features
- Automated text analysis and classification
- Customizable agent configurations via `agent_config.json`
- Seamless integration with OpenAI API
- Supports `.env` file for secure API key management

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/jacksonlmakl/redflag-nlp.git
   cd redflag-nlp
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, you need to add your OpenAI API key.

1. Create a `.env` file in the project root and add the following line:
   ```ini
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Ensure the `.env` file is not tracked by Git to keep your credentials secure. This repository already includes a `.gitignore` rule for `.env` files.

## Usage

To run the NLP agent:
```sh
python main.py
```

By default, the agent uses the settings from `agent_config.json`. Modify this file to customize behavior.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or issues, open an issue in the GitHub repository or contact [Jackson Makl](mailto:jackson.makl@dataiku.com).

