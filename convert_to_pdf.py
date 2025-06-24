#!/usr/bin/env python3
"""
Convert the YUM Email Categorizer guide from Markdown to PDF
"""

import markdown
import pdfkit
import os
import sys

def convert_markdown_to_pdf(markdown_file, output_file):
    """Convert markdown file to PDF"""
    try:
        # Read the markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML
        html = markdown.markdown(
            markdown_content,
            extensions=['toc', 'tables', 'fenced_code']
        )
        
        # Add CSS styling for better PDF appearance
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>YUM Email Categorizer - Complete User Guide</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #ecf0f1;
                    padding-bottom: 5px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #2c3e50;
                    margin-top: 25px;
                }}
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    padding: 15px;
                    overflow-x: auto;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 0;
                    padding-left: 20px;
                    color: #7f8c8d;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                .toc {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                .toc ul {{
                    list-style-type: none;
                    padding-left: 0;
                }}
                .toc li {{
                    margin: 5px 0;
                }}
                .toc a {{
                    text-decoration: none;
                    color: #3498db;
                }}
                .toc a:hover {{
                    text-decoration: underline;
                }}
                @page {{
                    margin: 1in;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Configure PDF options
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Convert HTML to PDF
        pdfkit.from_string(styled_html, output_file, options=options)
        
        print(f"✅ Successfully converted {markdown_file} to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

def main():
    """Main function"""
    markdown_file = "YUM_Email_Categorizer_Complete_Guide.md"
    output_file = "YUM_Email_Categorizer_Complete_Guide.pdf"
    
    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        print(f"❌ Error: {markdown_file} not found!")
        sys.exit(1)
    
    print(f"🔄 Converting {markdown_file} to PDF...")
    
    # Convert to PDF
    success = convert_markdown_to_pdf(markdown_file, output_file)
    
    if success:
        print(f"📄 PDF guide created: {output_file}")
        print(f"📊 File size: {os.path.getsize(output_file)} bytes")
    else:
        print("❌ Failed to create PDF")
        sys.exit(1)

if __name__ == "__main__":
    main()