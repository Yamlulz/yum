#!/usr/bin/env python3
"""
Create a package of all YUM Email Categorizer files for GitHub upload
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_github_package():
    """Create a clean package for GitHub upload"""
    
    # Create a temporary directory for the package
    package_dir = Path("yumcat_github_package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Files to include (all important files)
    files_to_copy = [
        # Main application
        "backend/app.py",
        "backend/categoriser.py", 
        "backend/email_generator.py",
        "backend/data/categories.json",
        "backend/data/feedback.json",
        
        # UI
        "ui/cli_test.py",
        
        # Setup scripts
        "setup_local_llm.sh",
        "setup_external_llm.py",
        
        # Training and demo
        "generate_training_emails.py",
        "email_training_tool.py",
        "demo_workflow.py",
        
        # Simple generators
        "generate_email.sh",
        "generate_realistic_emails.sh",
        
        # Documentation
        "README.md",
        "SIMPLE_SETUP_GUIDE.md",
        "EXTERNAL_LLM_GUIDE.md",
        "SHARING_GUIDE.md",
        "GITHUB_UPLOAD_GUIDE.md",
        "YUM_Email_Categorizer_Complete_Guide.md",
        
        # Utilities
        "convert_to_pdf.py",
        ".gitignore"
    ]
    
    # Copy files maintaining directory structure
    for file_path in files_to_copy:
        src = Path(file_path)
        if src.exists():
            dst = package_dir / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ Copied: {file_path}")
        else:
            print(f"⚠️  Not found: {file_path}")
    
    # Create a ZIP file for easy upload
    zip_path = "yumcat_for_github.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Package created successfully!")
    print(f"📁 Folder: {package_dir}")
    print(f"📦 ZIP file: {zip_path}")
    print(f"\n📋 Next steps:")
    print(f"1. Go to https://github.com/Yamlulz")
    print(f"2. Click 'New' to create a repository named 'yumcat'")
    print(f"3. Upload the files from '{package_dir}' folder")
    print(f"4. Or extract '{zip_path}' and upload those files")
    
    # Create a simple upload instruction file
    with open(package_dir / "UPLOAD_INSTRUCTIONS.md", "w") as f:
        f.write("""# Upload Instructions for GitHub

## Quick Upload Steps:

1. **Create Repository:**
   - Go to https://github.com/Yamlulz
   - Click "New" repository
   - Name: `yumcat`
   - Description: "AI-powered email categorization system for business emails"
   - Make it Public
   - Click "Create repository"

2. **Upload Files:**
   - On the new repository page, click "uploading an existing file"
   - Drag and drop ALL files from this folder
   - Add commit message: "Initial upload of YUM Email Categorizer"
   - Click "Commit changes"

3. **Verify Upload:**
   - Check that all folders (backend/, ui/) are present
   - Verify README.md displays correctly
   - Test that setup scripts are executable

## File Structure:
```
yumcat/
├── README.md                    # Main documentation
├── SIMPLE_SETUP_GUIDE.md        # Beginner guide
├── backend/                     # Core application
│   ├── app.py                  # Flask server
│   ├── categoriser.py          # AI classification
│   └── data/                   # Data files
├── ui/                         # User interface
├── setup_local_llm.sh          # LLM setup
└── [other files...]
```

## After Upload:
- Share the link: https://github.com/Yamlulz/yumcat
- Add topics: email-classification, ai, python, flask
- Create first release (v1.0.0)
""")
    
    print(f"📄 Upload instructions created: {package_dir}/UPLOAD_INSTRUCTIONS.md")

if __name__ == "__main__":
    create_github_package()