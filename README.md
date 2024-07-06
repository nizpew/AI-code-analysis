# Code Analyzer

## Overview
The Code Analyzer application is designed to analyze and explain code files using an AI-powered tool called TGPT. It provides both general analysis of the entire code file and specific line-by-line explanations interactively through a graphical user interface (GUI).
OS supported: Woks on Linux.


https://github.com/nizpew/AI-code-analysis/assets/144165519/b5acd13a-ffe2-43c4-8c3f-c1468d21b4a7




## Features
- **Import Code File**: Allows users to select and import a code file (e.g., Python script) for analysis.
- **Display and Analysis**: Displays the imported code in a scrollable text view within the GUI and provides analysis results directly within the interface.
- **Interactive Analysis**:
  - Clicking on specific lines in the displayed code triggers TGPT to provide explanations for those lines.
  - Outputs from TGPT are formatted and displayed in a structured manner in the GUI.
- **Error Handling**: Handles errors gracefully, including timeouts and unexpected issues during the analysis process.

## Dependencies
- **Python Libraries**:
  - `gi`: GObject introspection library for GTK integration.
  - `subprocess`: For executing TGPT commands and managing processes.
  - `threading`: Facilitates multi-threading for non-blocking UI interaction.
  - `tempfile`, `os`: For temporary file management and path operations.

## Usage
1. **Installation**:
   - Ensure Python and necessary dependencies are installed (`gi`, `subprocess`, etc.).
   -     curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s /usr/local/bin           #TGPT tool should be installed and accessible via the command line (`tgpt`).

2. **Execution**:
   - Run the script (`code_analyzer.py`). with "python staticcodenalysis.py" or "python3 staticcodenalysis.py" 
   - GUI will open, prompting to import a code file.
   - Clicking "Import Code File" allows selection of a file for analysis.
   - Clicking on specific lines within the displayed code triggers line-specific explanations. (Warning: BETA. may not work properly)

3. **Output**:
   - TGPT outputs are displayed in the GUI, formatted to distinguish code snippets, headers, and text explanations.

## Limitations
- Requires internet connectivity and access to TGPT for online processing.
- Currently supports analysis of textual code files; additional formats may require adaptation.

## Contributing
Contributions are welcome! Feel free to fork this repository, make enhancements, and submit a pull request.
