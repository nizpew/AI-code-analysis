import gi
import subprocess
import threading
import tempfile
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class CodeAnalyzer(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Code Analyzer")
        self.set_default_size(600, 400)
        self.filepath = None  # Initialize filepath attribute

        # Create a grid layout
        grid = Gtk.Grid()
        self.add(grid)

        # Create a button to import code file
        self.button = Gtk.Button(label="Import Code File")
        self.button.connect("clicked", self.on_file_clicked)
        grid.attach(self.button, 0, 0, 1, 1)

        # Create a scrolled text view to display code and analysis results
        self.textview = Gtk.TextView()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.textview)
        grid.attach(scrolled_window, 0, 1, 1, 1)

        # Connect click event to TextView
        self.textview.connect("button-release-event", self.on_textview_clicked)

        # Initialize temporary file path variable
        self.temp_filepath = None

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filepath = dialog.get_filename()  # Set the filepath attribute
            threading.Thread(target=self.analyze_code, args=(self.filepath,)).start()

        dialog.destroy()

    def on_textview_clicked(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == Gdk.BUTTON_PRIMARY:
            buffer = self.textview.get_buffer()
            mark = buffer.get_insert()
            iter = buffer.get_iter_at_mark(mark)
            line_number = iter.get_line()
            self.analyze_line(line_number)

    def analyze_code(self, filepath):
        try:
            # Construct the tgpt command with input redirection
            tgpt_command = f"cat '{filepath}' | tgpt -q 'Explain the code'"

            # Open subprocess with PIPEs
            tgpt_process = subprocess.Popen(tgpt_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Communicate with tgpt
            tgpt_output, tgpt_error = tgpt_process.communicate(timeout=60)

            if tgpt_output:
                # Save the initial tgpt output to a temporary file
                self.save_to_tempfile(tgpt_output)

                # Update GUI with formatted and annotated output
                formatted_output = self.format_tgpt_output(tgpt_output)
                Gdk.threads_enter()
                buffer = self.textview.get_buffer()
                buffer.set_text(formatted_output)
                Gdk.threads_leave()

            if tgpt_error:
                Gdk.threads_enter()
                buffer = self.textview.get_buffer()
                buffer.set_text(f"Error from tgpt: {tgpt_error}")
                Gdk.threads_leave()

        except subprocess.TimeoutExpired:
            print("tgpt command took too long to respond.")
            tgpt_process.kill()
            Gdk.threads_enter()
            buffer = self.textview.get_buffer()
            buffer.set_text("Explanation request timed out. Please try again.")
            Gdk.threads_leave()

        except Exception as e:
            print(f"An error occurred: {e}")
            Gdk.threads_enter()
            buffer = self.textview.get_buffer()
            buffer.set_text(f"An error occurred: {e}")
            Gdk.threads_leave()

    def save_to_tempfile(self, content):
        # Create or overwrite the temporary file with the given content
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(content)
            self.temp_filepath = temp_file.name

    def analyze_line(self, line_number):
        try:
            if not self.temp_filepath or not os.path.exists(self.temp_filepath):
                raise ValueError("No initial tgpt output file found.")

            # Construct the tgpt command for line-specific explanation using the saved file
            tgpt_command = f"cat '{self.temp_filepath}' | tgpt -q 'Explain line {line_number} of this file'"

            # Open subprocess with PIPEs
            tgpt_process = subprocess.Popen(tgpt_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Communicate with tgpt
            tgpt_output, tgpt_error = tgpt_process.communicate(timeout=60)

            if tgpt_output:
                Gdk.threads_enter()
                buffer = self.textview.get_buffer()
                buffer.set_text(tgpt_output)
                Gdk.threads_leave()

            if tgpt_error:
                Gdk.threads_enter()
                buffer = self.textview.get_buffer()
                buffer.set_text(f"Error from tgpt: {tgpt_error}")
                Gdk.threads_leave()

        except subprocess.TimeoutExpired:
            print(f"tgpt command for line {line_number} took too long to respond.")
            tgpt_process.kill()
            Gdk.threads_enter()
            buffer = self.textview.get_buffer()
            buffer.set_text(f"Explanation request for line {line_number} timed out. Please try again.")
            Gdk.threads_leave()

        except Exception as e:
            print(f"An error occurred: {e}")
            Gdk.threads_enter()
            buffer = self.textview.get_buffer()
            buffer.set_text(f"An error occurred: {e}")
            Gdk.threads_leave()

    def format_tgpt_output(self, output):
        # Split output by sections based on code blocks
        sections = output.split("\n\n")
        formatted_output = []

        for section in sections:
            if section.strip().startswith("###"):
                # Format section headers
                formatted_output.append(f"\n{section.strip()}\n")
            elif section.strip().startswith("```"):
                # Format code snippets
                formatted_output.append(f"\n{section.strip()}\n")
            else:
                # Add regular text with proper indentation
                formatted_lines = ["    " + line.strip() for line in section.splitlines() if line.strip()]
                formatted_output.extend(formatted_lines)
                formatted_output.append("")  # Add empty line for separation

        return "\n".join(formatted_output)

def main():
    win = CodeAnalyzer()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

