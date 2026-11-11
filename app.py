import os
import csv
import tkinter as tk

from tkinter import ttk, filedialog, messagebox

from main import preview_client_folder, get_preview_summary
from config import TEST_MODE
from organization.file_mover import move_document
from organization.processing_logger import log_document
from organization.processing_logger import LOG_FILE
from classification.document_identifier import DOCUMENT_REGISTRIES
from organization.file_naming import generate_filename
from organization.folder_routing import get_destination_folder


class DocumentOrganizerApp:

    def __init__(self, root):

        self.root = root

        self.root.title("PDF Document Organizer")
        self.root.geometry("1150x780")
        self.root.minsize(900, 600)

        self.client_folder = tk.StringVar()
        self.status_message = tk.StringVar(
            value="Select a client folder to get started."
        )

        self.selected_document_type = tk.StringVar()
        self.destination_folder = tk.StringVar()

        self.results = []

        # Get all document types from the existing registries
        self.document_types = sorted({
            document_type
            for registry in DOCUMENT_REGISTRIES.values()
            for document_type in registry
        })

        self.create_interface()

    def create_interface(self):

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        main_frame = ttk.Frame(canvas, padding=20)

        canvas_window = canvas.create_window(
            (0, 0),
            window=main_frame,
            anchor="nw"
        )

        main_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width
            )
        )

        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        title = ttk.Label(
            main_frame,
            text="PDF Document Organizer",
            font=("Arial", 22, "bold")
        )

        title.pack(anchor="w")

        subtitle = ttk.Label(
            main_frame,
            text="Automatically classify and organize accounting documents."
        )

        subtitle.pack(anchor="w", pady=(5, 20))

        # Client folder selection
        folder_frame = ttk.LabelFrame(
            main_frame,
            text="Select Client Folder",
            padding=12
        )

        folder_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.client_folder,
            font=("Arial", 10)
        )

        folder_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ttk.Button(
            folder_frame,
            text="Browse",
            command=self.browse_folder
        ).pack(side="right")

        # Preview controls
        controls_frame = ttk.Frame(main_frame)

        controls_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Button(
            controls_frame,
            text="Preview Documents",
            command=self.preview_documents
        ).pack(side="left")
        
        ttk.Button(
            controls_frame,
            text="Approve & Process",
            command=self.approve_documents
        ).pack(side="left", padx=10)
        
        ttk.Button(
            controls_frame,
            text="Processing History",
            command=self.show_processing_history
        ).pack(side="left")

        # Summary section
        summary_frame = ttk.LabelFrame(
            main_frame,
            text="Processing Summary",
            padding=12
        )

        summary_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.total_label = ttk.Label(
            summary_frame,
            text="Total: 0"
        )

        self.total_label.pack(side="left", padx=(0, 30))

        self.classified_label = ttk.Label(
            summary_frame,
            text="Classified: 0"
        )

        self.classified_label.pack(side="left", padx=(0, 30))

        self.review_label = ttk.Label(
            summary_frame,
            text="Review: 0"
        )

        self.review_label.pack(side="left", padx=(0, 30))

        self.failed_label = ttk.Label(
            summary_frame,
            text="Failed: 0"
        )

        self.failed_label.pack(side="left")

        # Document preview table
        table_frame = ttk.LabelFrame(
            main_frame,
            text="Document Preview",
            padding=10
        )

        table_frame.pack(
            fill="both",
            expand=True,
            pady=(0, 15)
        )

        columns = (
            "original",
            "document_type",
            "confidence",
            "new_filename",
            "destination"
        )

        self.document_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.document_table.heading(
            "original",
            text="Original Filename"
        )

        self.document_table.heading(
            "document_type",
            text="Document Type"
        )

        self.document_table.heading(
            "confidence",
            text="Confidence"
        )

        self.document_table.heading(
            "new_filename",
            text="Proposed Filename"
        )

        self.document_table.heading(
            "destination",
            text="Destination Folder"
        )

        self.document_table.column("original", width=170)
        self.document_table.column("document_type", width=140)
        self.document_table.column(
            "confidence",
            width=110,
            anchor="center"
        )
        self.document_table.column("new_filename", width=210)
        self.document_table.column("destination", width=190)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.document_table.yview
        )

        self.document_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.document_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.document_table.tag_configure(
            "review",
            background="#fff0d6"
        )

        self.document_table.tag_configure(
            "failed",
            background="#f8d7da"
        )

        self.document_table.bind(
            "<<TreeviewSelect>>",
            self.show_document_details
        )

        # Selected document details
        details_frame = ttk.LabelFrame(
            main_frame,
            text="Selected Document Details",
            padding=10
        )

        details_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.details_label = ttk.Label(
            details_frame,
            text="Select a document above to view its details.",
            justify="left",
            wraplength=1050
        )

        self.details_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # Classification correction
        correction_frame = ttk.Frame(details_frame)

        correction_frame.pack(
            fill="x",
            pady=(0, 8)
        )

        ttk.Label(
            correction_frame,
            text="Correct document type:"
        ).pack(side="left", padx=(0, 8))

        self.document_type_dropdown = ttk.Combobox(
            correction_frame,
            textvariable=self.selected_document_type,
            values=self.document_types,
            state="readonly",
            width=35
        )

        self.document_type_dropdown.pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            correction_frame,
            text="Apply Classification",
            command=self.apply_classification
        ).pack(side="left")

        # Destination correction
        destination_frame = ttk.Frame(details_frame)

        destination_frame.pack(fill="x")

        ttk.Label(
            destination_frame,
            text="Destination:"
        ).pack(side="left", padx=(0, 8))

        destination_entry = ttk.Entry(
            destination_frame,
            textvariable=self.destination_folder,
            state="readonly"
        )

        destination_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ttk.Button(
            destination_frame,
            text="Choose Folder",
            command=self.choose_destination
        ).pack(side="right")

        # Application status
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_message,
            font=("Arial", 9)
        )

        status_label.pack(anchor="w")

    def browse_folder(self):

        selected_folder = filedialog.askdirectory(
            title="Select Client Folder"
        )

        if selected_folder:

            self.client_folder.set(selected_folder)

            self.status_message.set(
                "Client folder selected. Ready to preview."
            )

    def preview_documents(self):

        folder = self.client_folder.get().strip()

        if not folder:

            messagebox.showwarning(
                "Folder Required",
                "Please select a client folder first."
            )

            return

        if not os.path.isdir(folder):

            messagebox.showerror(
                "Invalid Folder",
                "The selected folder does not exist."
            )

            return

        self.status_message.set(
            "Reading and analyzing documents..."
        )

        self.root.config(cursor="watch")
        self.root.update_idletasks()

        try:

            self.results = preview_client_folder(folder)

            self.refresh_table()

            summary = get_preview_summary(self.results)

            self.update_summary(summary)

            self.details_label.config(
                text="Select a document above to view its details."
            )

            self.selected_document_type.set("")
            self.destination_folder.set("")

            self.status_message.set(
                f"Preview complete. {summary['total']} documents analyzed. "
                "No files have been moved."
            )

        except Exception as error:

            messagebox.showerror(
                "Processing Error",
                str(error)
            )

            self.status_message.set(
                "An error occurred during document processing."
            )

        finally:

            self.root.config(cursor="")

    def refresh_table(self):

        self.document_table.delete(
            *self.document_table.get_children()
        )

        for index, result in enumerate(self.results):

            if result["status"] == "Failed":
                tag = "failed"

            elif result["status"] == "Review":
                tag = "review"

            else:
                tag = ""

            self.document_table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    result["original_filename"],
                    result["document_type"],
                    result["confidence"],
                    result["new_filename"],
                    os.path.basename(result["destination_folder"])
                ),
                tags=(tag,)
            )

    def update_summary(self, summary):

        self.total_label.config(
            text=f"Total: {summary['total']}"
        )

        self.classified_label.config(
            text=f"Classified: {summary['classified']}"
        )

        self.review_label.config(
            text=f"Review: {summary['review']}"
        )

        self.failed_label.config(
            text=f"Failed: {summary['failed']}"
        )

    def get_selected_index(self):

        selected = self.document_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Document Selected",
                "Please select a document from the preview table first."
            )

            return None

        return int(selected[0])

    def get_unique_preview_destination(
        self,
        destination_folder,
        filename,
        selected_index
    ):

        name, extension = os.path.splitext(filename)

        destination_path = os.path.join(
            destination_folder,
            filename
        )

        reserved_paths = set()

        # Collect destinations assigned to other preview documents
        for index, result in enumerate(self.results):

            if index == selected_index:
                continue

            if result.get("destination_path"):

                reserved_paths.add(
                    os.path.normcase(
                        os.path.abspath(result["destination_path"])
                    )
                )

        counter = 2

        while (
            os.path.exists(destination_path)
            or os.path.normcase(os.path.abspath(destination_path))
            in reserved_paths
        ):

            new_filename = f"{name}_{counter}{extension}"

            destination_path = os.path.join(
                destination_folder,
                new_filename
            )

            counter += 1

        return destination_path
    
    def show_processing_history(self):

        if not os.path.isfile(LOG_FILE):

            messagebox.showinfo(
                "Processing History",
                "No processing history is available yet."
            )

            return

        try:

            with open(
                LOG_FILE,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                reader = csv.DictReader(file)
                history = list(reader)
                columns = reader.fieldnames

            if not history or not columns:

                messagebox.showinfo(
                    "Processing History",
                    "The processing history file is empty."
                )

                return

            history_window = tk.Toplevel(self.root)

            history_window.title("Processing History")
            history_window.geometry("1100x550")
            history_window.minsize(750, 350)

            frame = ttk.Frame(
                history_window,
                padding=15
            )

            frame.pack(
                fill="both",
                expand=True
            )

            ttk.Label(
                frame,
                text=f"Processing History — {len(history)} records",
                font=("Arial", 15, "bold")
            ).pack(anchor="w", pady=(0, 12))

            table_frame = ttk.Frame(frame)

            table_frame.pack(
                fill="both",
                expand=True
            )

            history_table = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings"
            )

            for column in columns:

                history_table.heading(
                    column,
                    text=column.replace("_", " ").title()
                )

                history_table.column(
                    column,
                    width=150,
                    minwidth=100
                )

            vertical_scrollbar = ttk.Scrollbar(
                table_frame,
                orient="vertical",
                command=history_table.yview
            )

            horizontal_scrollbar = ttk.Scrollbar(
                table_frame,
                orient="horizontal",
                command=history_table.xview
            )

            history_table.configure(
                yscrollcommand=vertical_scrollbar.set,
                xscrollcommand=horizontal_scrollbar.set
            )

            history_table.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            vertical_scrollbar.grid(
                row=0,
                column=1,
                sticky="ns"
            )

            horizontal_scrollbar.grid(
                row=1,
                column=0,
                sticky="ew"
            )

            table_frame.rowconfigure(0, weight=1)
            table_frame.columnconfigure(0, weight=1)

            for record in history:

                history_table.insert(
                    "",
                    "end",
                    values=[
                        record.get(column, "")
                        for column in columns
                    ]
                )

        except Exception as error:

            messagebox.showerror(
                "History Error",
                f"Could not open processing history:\n\n{error}"
            )


    def approve_documents(self):

        if not self.results:
            messagebox.showwarning(
                "No Preview Available",
                "Please preview a client folder before processing."
            )
            return

        approved_count = sum(
            1 for result in self.results
            if result["status"] == "Classified"
        )

        skipped_count = len(self.results) - approved_count

        if approved_count == 0:
            messagebox.showwarning(
                "No Documents to Process",
                "There are no classified documents ready for processing."
            )
            return

        if TEST_MODE:
            confirmation_message = (
                f"{approved_count} classified documents will be simulated.\n\n"
                "TEST MODE is enabled. No original files will be moved.\n\n"
                f"{skipped_count} documents will be skipped because they "
                "require review or have errors.\n\n"
                "Continue?"
            )
        else:
            confirmation_message = (
                f"{approved_count} classified documents will be moved.\n\n"
                "Original PDFs will be moved into their assigned folders.\n\n"
                f"{skipped_count} documents will be skipped because they "
                "require review or have errors.\n\n"
                "Continue?"
            )

        approved = messagebox.askyesno(
            "Confirm Processing",
            confirmation_message
        )

        if not approved:
            return

        previewed = 0
        moved = 0
        failed = 0
        skipped = 0

        client = os.path.basename(
            os.path.normpath(self.client_folder.get())
        )

        for result in self.results:

            information = {
                "category": result["category"],
                "document_type": result["document_type"],
                "confidence": result["confidence"],
                "status": result["status"],
                "company": result.get("company"),
                "institution": result.get("institution"),
                "tax_year": result.get("tax_year"),
                "month_year": result.get("month_year")
            }

            if result["status"] != "Classified":

                skipped += 1

                log_document(
                    information,
                    client,
                    result["original_filename"],
                    result["new_filename"],
                    result.get("destination_path"),
                    "Skipped",
                    "Document requires review or has a processing error."
                )

                result["processing_result"] = "Skipped"
                continue

            outcome = move_document(
                result["source_path"],
                result["destination_folder"],
                result["new_filename"]
            )

            processing_status = outcome["status"]

            if processing_status == "Preview":
                previewed += 1

            elif processing_status == "Moved":
                moved += 1

            else:
                failed += 1

            result["processing_result"] = processing_status

            actual_destination = outcome.get(
                "destination",
                result.get("destination_path")
            )

            log_document(
                information,
                client,
                result["original_filename"],
                result["new_filename"],
                actual_destination,
                processing_status,
                outcome.get("message", "")
            )

        if TEST_MODE:

            message = (
                f"Test processing complete.\n\n"
                f"Previewed: {previewed}\n"
                f"Skipped: {skipped}\n"
                f"Failed: {failed}\n\n"
                "No original files were moved."
            )

        else:

            message = (
                f"Processing complete.\n\n"
                f"Moved: {moved}\n"
                f"Skipped: {skipped}\n"
                f"Failed: {failed}"
            )

        self.status_message.set(
            "Processing complete. See the processing history log."
        )

        messagebox.showinfo(
            "Processing Results",
            message
        )


    def show_document_details(self, event):

        selected = self.document_table.selection()

        if not selected:
            return

        index = int(selected[0])
        result = self.results[index]

        self.selected_document_type.set(
            result["document_type"]
        )

        self.destination_folder.set(
            result["destination_folder"]
        )

        details = (
            f"Original file: {result['original_filename']}\n"
            f"Document type: {result['document_type']}\n"
            f"Category: {result['category']}\n"
            f"Confidence: {result['confidence']}\n"
            f"Company: {result['company'] or 'Not identified'}\n"
            f"Institution: {result['institution'] or 'Not identified'}\n"
            f"Tax year: {result['tax_year'] or 'Not identified'}\n"
            f"Month/year: {result['month_year'] or 'Not identified'}\n"
            f"Proposed filename: {result['new_filename']}\n"
            f"Destination: {result['destination_folder']}\n"
            f"Error: {result['error'] or 'None'}"
        )

        self.details_label.config(text=details)

    def apply_classification(self):

        index = self.get_selected_index()

        if index is None:
            return

        document_type = self.selected_document_type.get()

        if not document_type:
            messagebox.showwarning(
                "Document Type Required",
                "Please select a document type."
            )

            return

        # Find the category associated with the selected document type
        category = None

        for registry_category, registry in DOCUMENT_REGISTRIES.items():

            if document_type in registry:
                category = registry_category
                break

        if category is None:
            messagebox.showerror(
                "Classification Error",
                "The selected document type was not found."
            )

            return

        result = self.results[index]

        # Build updated information for filename and folder routing
        information = {
            "category": category,
            "document_type": document_type,
            "tax_year": result.get("tax_year"),
            "month_year": result.get("month_year"),
            "institution": result.get("institution"),
            "company": result.get("company")
        }

        new_filename = generate_filename(
            information,
            result["original_filename"]
        )

        destination_folder = get_destination_folder(
            self.client_folder.get(),
            {
                "category": category,
                "document_type": document_type,
                "status": "Classified"
            }
        )

        destination_path = self.get_unique_preview_destination(
            destination_folder,
            new_filename,
            index
        )

        # Update the preview result
        result["document_type"] = document_type
        result["category"] = category
        result["confidence"] = "Manually reviewed"
        result["status"] = "Classified"
        result["new_filename"] = os.path.basename(destination_path)
        result["destination_folder"] = destination_folder
        result["destination_path"] = destination_path
        result["error"] = None

        self.refresh_table()
        self.update_summary(get_preview_summary(self.results))

        self.document_table.selection_set(str(index))
        self.document_table.focus(str(index))

        self.show_document_details(None)

        self.status_message.set(
            "Classification corrected. No files have been moved."
        )

    def choose_destination(self):

        index = self.get_selected_index()

        if index is None:
            return

        result = self.results[index]

        selected_folder = filedialog.askdirectory(
            title="Choose Destination Folder",
            initialdir=result["destination_folder"]
        )

        if not selected_folder:
            return

        destination_path = self.get_unique_preview_destination(
            selected_folder,
            result["new_filename"],
            index
        )

        result["destination_folder"] = selected_folder
        result["destination_path"] = destination_path
        result["new_filename"] = os.path.basename(destination_path)

        self.refresh_table()

        self.document_table.selection_set(str(index))
        self.document_table.focus(str(index))

        self.show_document_details(None)

        self.status_message.set(
            "Destination updated. No files have been moved."
        )


def main():

    root = tk.Tk()

    app = DocumentOrganizerApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
