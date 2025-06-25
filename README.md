# Codex-Reader

**Logline:** A minimalist interface for the deep reading and semantic analysis of complex texts and AI-generated transcripts.

---

### Description

The Codex Reader is a lightweight, browser-based reading environment designed for scholars, researchers, and analysts working with dense, structured documents. It transforms raw JSON transcripts into a clean, interactive, and semantically-rich format, with a focus on citation management, toggling between AI reasoning and final output, and rendering complex data like tables and diagrams. Its warm, archival aesthetic is designed to reduce eye strain and encourage long-form reading and analysis.

### Key Features

*   **Semantic Content Rendering**: Intelligently distinguishes between an AI's preliminary "reasoning trace" and its final "completion," displaying them in distinct, toggleable sections.
*   **Stable Citation System**: Automatically assigns a unique, sequential number to every paragraph, which is displayed neatly in the margin. The citation numbers are stable, interactive, and do not disrupt the flow of the text.
*   **Interactive Diagrams**: Renders `mermaid` code blocks as fully interactive SVG diagrams. A toggle allows the user to switch between the visual graph and the underlying code.
*   **Advanced Markdown Parsing**: 
    *   Correctly renders tables with enhanced styling for readability.
    *   Respects line breaks (`<br>` tags and newlines) within tables and other content.
    *   Supports custom `<tag>` syntax, rendering it as literal text rather than stripping it as invalid HTML.
*   **Modern, Focused UI**: Features a clean, minimalist design with a warm, paper-like aesthetic to create a comfortable long-form reading experience.
*   **Dynamic Paper Loading**: On launch, the reader presents a clean selection screen to choose from any `.json` transcript in the directory. Papers can also be loaded directly via URL parameters.

### How It Works

The entire application is a self-contained HTML file that runs in any modern web browser. It requires no build process or external dependencies beyond the included CDN links for `marked.js`, `DOMPurify`, and `Mermaid.js`.

1.  **Initialization**: On load, the script waits for the Mermaid.js library to be fully ready using a robust polling mechanism to prevent race conditions.
2.  **Data Fetching**: If no paper is specified in the URL, the app fetches a list of all `.json` files in the current directory and displays them on a selection screen.
3.  **Content Parsing & Rendering**: When a paper is loaded, the JavaScript logic:
    *   Fetches and parses the selected JSON transcript.
    *   Iterates through the `model` completions, separating the reasoning trace (first part) from the main content (subsequent parts).
    *   Uses `marked.js` with a custom extension to convert the Markdown content into sanitized HTML. This process correctly handles tables, line breaks, and custom tags.
    *   Injects the rendered HTML into the document, assigning citation numbers to each citable element.
    *   Calls the `enhanceContent()` function to find and render any Mermaid diagrams.

### File Structure

*   `reader-codex-08.html`: The main, self-contained web application. This is the file you open in your browser.
*   `*.json`: The JSON transcript files that serve as the data source for the reader.

### How to Use

1.  **Place Files**: Ensure that your `reader-codex-08.html` file and your `.json` transcript files are in the same directory.
2.  **Start a Web Server**: Because the reader fetches data files, it must be run from a local web server.
    ```bash
    # Navigate to your project directory in the terminal
    cd /path/to/your/project
    
    # Start a simple Python web server
    python3 -m http.server 8000
    ```
3.  **Open the Reader**: Navigate to the following URL in your web browser:
    [http://localhost:8000/reader-codex-08.html](http://localhost:8000/reader-codex-08.html)
