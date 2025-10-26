import flet as ft
import requests
import base64
import json
from datetime import datetime
from snackbar import Snackbar
import os

class SubmitBug(ft.AlertDialog):
    def __init__(self, page):
        self.page = page
        self.message_field = ft.TextField(
            label="Bug Description", 
            multiline=True,
            min_lines=3,
            hint_text="Describe the bug in detail...",
        )
        
        self.title_field = ft.TextField(
            label="Issue Title",
            hint_text="Brief description of the issue"
        )
        
        # Optional: Add issue type selector
        self.issue_type = ft.Dropdown(
            label="Issue Type",
            options=[
                ft.dropdown.Option("bug"),
                ft.dropdown.Option("enhancement"),
                ft.dropdown.Option("question"),
            ],
            value="bug"
        )
        
        super().__init__(
            modal=True,
            title=ft.Text("Submit Bug Report", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                self.title_field,
                self.issue_type,
                self.message_field,
            ], 
            height=300, 
            width=400,
            scroll=ft.ScrollMode.ADAPTIVE
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.ElevatedButton("Submit", on_click=self.submit_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
    def open_dialog(self, e=None):
        """Open the dialog"""
        self.page.dialog = self
        self.open = True
        self.page.update()

    def close_dialog(self, e=None):
        """Close the dialog"""
        self.open = False
        self.page.update()

    def create_github_issue(self, title, body, issue_type="bug"):
        """
        Create an issue in GitHub repository
        
        You'll need to configure these:
        - GITHUB_TOKEN: Personal access token with repo scope
        - REPO_OWNER: Your GitHub username or organization
        - REPO_NAME: Repository name
        """
        # Configuration - UPDATE THESE VALUES
        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
        REPO_OWNER = "pacopacev"
        REPO_NAME = "fletApp"
        
        
        if not GITHUB_TOKEN.startswith("ghp_"):
            return False, "GitHub token not configured"
        
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Create labels based on issue type
        labels = [issue_type]
        if issue_type == "bug":
            labels.extend(["bug-report", "triage"])
        elif issue_type == "enhancement":
            labels.extend(["feature-request", "enhancement"])
        
        data = {
            "title": title,
            "body": body,
            "labels": labels
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                issue_data = response.json()
                return True, f"Issue #{issue_data['number']} created successfully: {issue_data['html_url']}"
            else:
                return False, f"GitHub API error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, f"Network error: {str(e)}"

    def submit_dialog(self, e=None):
        """Handle form submission to GitHub"""
        if not self.title_field.value.strip():
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Please enter a title!"))
            )
            return
            
        if not self.message_field.value.strip():
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Please enter a description!"))
            )
            return
        
        # Show loading indicator
        self.submit_button_original_text = self.actions[1].text
        self.actions[1].text = "Submitting..."
        self.actions[1].disabled = True
        self.page.update()
        
        # Create issue body with additional context
        issue_body = f"""
### Bug Description
{self.message_field.value}

### Additional Context
- Reported via: Flet Application
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Issue Type: {self.issue_type.value}

---

*This issue was automatically generated from the application bug report form.*
        """.strip()
        
        # Submit to GitHub
        success, message = self.create_github_issue(
            title=self.title_field.value.strip(),
            body=issue_body,
            issue_type=self.issue_type.value
        )
        
        # Reset button state
        self.actions[1].text = self.submit_button_original_text
        self.actions[1].disabled = False
        
        if success:
            print(f"Bug submitted to GitHub Repo: {message}")
            # Clear fields
            self.title_field.value = ""
            self.message_field.value = ""
            self.close_dialog()
            snackbar_instance = Snackbar(f"{message}", bgcolor="green", length = None)
            snackbar_instance.open = True
            self.page.controls.append(snackbar_instance)
            self.page.update()
        
        else:
            print(f"Failed to submit bug: {message}")
            snackbar_instance = Snackbar(f"{message}", bgcolor="red", length = None)
            snackbar_instance.open = True
            self.page.controls.append(snackbar_instance)
            self.page.update()
        
        self.page.update()