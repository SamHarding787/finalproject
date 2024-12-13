import csv
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
from SamHarding2 import *


class GradeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Hide all attempt fields, errors, and success messages initially
        self.hide_attempt_fields()
        self.ui.label_2.setVisible(False)  # General error message
        self.ui.submitSuccess.setVisible(False)  # Success message

        # Connect number of attempts field to dynamically show fields
        self.ui.attemptNumberEdit.textChanged.connect(self.update_attempt_fields)

        # Connect the Submit button
        self.ui.Submit_Button.clicked.connect(self.process_grades)

    def hide_attempt_fields(self):
        """Hide all attempt input fields, error labels, and success messages."""
        for i in range(1, 5):
            getattr(self.ui, f"attempt{i}edit").setVisible(False)  # Hide input fields
            getattr(self.ui, f"attempt{i}text").setVisible(False)  # Hide labels
            getattr(self.ui, f"attempt{i}error").setVisible(False)  # Hide error labels
        self.ui.label_2.setVisible(False)  # Hide general error message
        self.ui.submitSuccess.setVisible(False)  # Hide success message

    def update_attempt_fields(self):
        """Update visibility of attempt fields based on the number of attempts."""
        # Hide all attempt fields and errors initially
        self.hide_attempt_fields()

        try:
            num_attempts = int(self.ui.attemptNumberEdit.text())
        except ValueError:
            num_attempts = 0

        # Ensure the number of attempts is within the valid range (1–4)
        num_attempts = max(0, min(4, num_attempts))

        # Show or hide fields dynamically
        for i in range(1, 5):
            visible = i <= num_attempts
            getattr(self.ui, f"attempt{i}edit").setVisible(visible)  # Show/Hide input fields
            getattr(self.ui, f"attempt{i}text").setVisible(visible)  # Show/Hide labels

    def validate_inputs(self):
        """Validate all inputs before processing grades."""
        self.ui.label_2.setVisible(False)  # Hide general error message
        errors = False

        # Validate student name
        if not self.ui.studentNameEdit.text().strip():
            self.ui.nameError.setVisible(True)
            errors = True
        else:
            self.ui.nameError.setVisible(False)

        # Validate number of attempts
        try:
            num_attempts = int(self.ui.attemptNumberEdit.text())
            if num_attempts < 1 or num_attempts > 4:
                self.ui.attemptError.setText("Attempts must be between 1 and 4")
                self.ui.attemptError.setVisible(True)
                errors = True
            else:
                self.ui.attemptError.setVisible(False)
        except ValueError:
            self.ui.attemptError.setText("Invalid number of attempts")
            self.ui.attemptError.setVisible(True)
            errors = True

        # Validate individual attempts
        for i in range(1, 5):
            attempt_field = getattr(self.ui, f"attempt{i}edit")
            attempt_error = getattr(self.ui, f"attempt{i}error")

            if i <= int(self.ui.attemptNumberEdit.text() or 0):  # Only check visible attempts
                try:
                    score = int(attempt_field.text())
                    if score < 0 or score > 100:
                        attempt_error.setText("Score must be 0-100")
                        attempt_error.setVisible(True)
                        errors = True
                    else:
                        attempt_error.setVisible(False)
                except ValueError:
                    attempt_error.setText("Invalid score")
                    attempt_error.setVisible(True)
                    errors = True

        if errors:
            self.ui.label_2.setText("Please fix all errors before submitting")
            self.ui.label_2.setVisible(True)

        return not errors

    def process_grades(self):
        """Handle grade processing and submission."""
        if not self.validate_inputs():
            self.ui.submitSuccess.setVisible(False)  # Hide success message if validation fails
            return

        # Hide general error message
        self.ui.label_2.setVisible(False)

        # Collect inputs
        student_name = self.ui.studentNameEdit.text()
        num_attempts = int(self.ui.attemptNumberEdit.text())
        scores = [int(getattr(self.ui, f"attempt{i}edit").text()) for i in range(1, num_attempts + 1)]
        best_grade = max(scores)

        # Calculate grades
        avg_score = calculate_average(scores)
        avg_grade = get_ave_grade(avg_score, best_grade)

        # Write to CSV
        self.write_to_csv(student_name, scores, avg_score, avg_grade)

        # Show success message
        self.ui.submitSuccess.setText("Submitted!")
        self.ui.submitSuccess.setVisible(True)

    def write_to_csv(self, student_name, scores, avg_score, avg_grade):
        """Write validated data to a CSV file."""
        file_name = "results.csv"
        headers = ["Student Name", "Scores", "Average Score", "Average Grade"]

        # Format data for CSV
        data = [student_name, ",".join(map(str, scores)), f"{avg_score:.2f}", avg_grade]

        # Append data to CSV
        try:
            with open(file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(headers)
                writer.writerow(data)
        except Exception as e:
            print(f"Error writing to CSV: {e}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = GradeApp()
    window.show()
    sys.exit(app.exec_())
