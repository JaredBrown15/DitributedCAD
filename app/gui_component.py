from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel
import sys
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import QTimer
import json
import requests

request_url = "https://api.jaredwjbrown.com"
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Distributed CAD")

main_layout = QVBoxLayout()



# Text Input Layout Defined Here
prompt_layout = QVBoxLayout()
input = QLineEdit()
input.setPlaceholderText("Enter your text prompt here (Ex: Generate me a model of a circular table")
input_label = QLabel("Enter Prompt Below")
input_label.setMaximumHeight(input_label.sizeHint().height())
input.setMaximumHeight(input.sizeHint().height())
input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


prompt_layout.addWidget(input_label)
prompt_layout.addWidget(input)
prompt_layout.setSpacing(0)
prompt_layout.setContentsMargins(0, 0, 0, 0)
main_layout.addLayout(prompt_layout)


model_dropdown_layout = QVBoxLayout()
model_dropdown = QComboBox()
model_dropdown.addItems(["WaLa", "Model 2", "Model 3"])
model_dropdown.setMaximumHeight(model_dropdown.sizeHint().height())
model_dropdown_label = QLabel("Select the model you would like to use:")
model_dropdown_label.setMaximumHeight(model_dropdown_label.sizeHint().height())
model_dropdown_layout.addWidget(model_dropdown_label)
model_dropdown_layout.addWidget(model_dropdown)
model_dropdown_layout.setSpacing(0)
model_dropdown_layout.setContentsMargins(0, 0, 0, 0)
model_dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
main_layout.addLayout(model_dropdown_layout)
model_dropdown.setEditable(False)


def on_model_selection(index):
    QTimer.singleShot(50, model_dropdown.hidePopup)
    model_dropdown.clearFocus()
    window.setFocus()

model_dropdown.activated.connect(on_model_selection)

def submit_task():
    data ={"prompt": input.text(),"model": model_dropdown.currentText()}
    json_data = json.dumps(data)
    print(json_data)
    response = requests.post(request_url, json=data)  # requests will handle json.dumps automatically
    # Get the JSON response
    json_result = response.json()
    print(json_result["filename"])
    #wala_input = json_result.get('WaLa_Input')
    submission_label.setText(f" You requested '{input.text()}'\n The model used for this request was '{model_dropdown.currentText()}'\n Json Response: '{json_result}'")
    #print(f"Returned JSON Response is: {wala_input}\n")



submission_button = QPushButton("Submit Task")
submission_button.clicked.connect(submit_task)
main_layout.addWidget(submission_button)
submission_label = QLabel("Submit a Prompt")
main_layout.addWidget(submission_label)

# main_layout.setSpacing(5)  # small space between sub-layouts
# main_layout.setContentsMargins(10, 10, 10, 10)  # optional padding around the window

window.setLayout(main_layout)
window.resize(2000, 1000)
window.show()

sys.exit(app.exec())







# import tkinter as tk
# from tkinter import ttk




# class ResponsiveApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.style = ttk.Style(self)
#         self.style.theme_use("alt")  # other options: 'default', 'alt', 'vista', 'xpnative'v
#         self.geometry("600x400")  # starting size
#         self.minsize(400, 250)    # prevent too small
    
#         # --- Configure grid layout ---
#         self.columnconfigure(0, weight=1)  # column expands
#         self.rowconfigure(0, weight=0)     # top label row fixed
#         self.rowconfigure(1, weight=0)     # entry + dropdown fixed
#         self.rowconfigure(2, weight=1)     # output frame grows

#         # --- Widgets ---
#         # Title Label
#         title_label = ttk.Label(self, text="Resizable GUI Example", font=("Segoe UI", 16))
#         title_label.grid(row=0, column=0, pady=10, sticky="n")

#         # Frame for inputs
#         input_frame = ttk.Frame(self)
#         input_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
#         input_frame.columnconfigure(0, weight=1)
#         input_frame.columnconfigure(1, weight=1)

#         # Text Entry
#         self.entry_var = tk.StringVar()
#         entry = ttk.Entry(input_frame, textvariable=self.entry_var)
#         entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

#         # Dropdown
#         self.selected_option = tk.StringVar(value="Option A")
#         dropdown = ttk.Combobox(input_frame, textvariable=self.selected_option, values=["Option A", "Option B", "Option C"])
#         dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

#         # Button
#         submit_button = ttk.Button(input_frame, text="Submit", command=self.on_submit)
#         submit_button.grid(row=0, column=2, padx=5, pady=5)

#         # Output Frame
#         output_frame = ttk.Frame(self, relief="groove")
#         output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
#         output_frame.columnconfigure(0, weight=1)
#         output_frame.rowconfigure(0, weight=1)

#         # Output Label (will resize with window)
#         self.output_label = ttk.Label(output_frame, text="Resize the window to see it adapt!", anchor="center")
#         self.output_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


#     def on_submit(self):
#         text = self.entry_var.get()
#         choice = self.selected_option.get()
#         if text.strip():
#             self.output_label.config(text=f"You entered '{text}' and selected '{choice}'.")
#         else:
#             self.output_label.config(text="Please enter some text.")

# if __name__ == "__main__":
#     app = ResponsiveApp()
#     app.mainloop()


