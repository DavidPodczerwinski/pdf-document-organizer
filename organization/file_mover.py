
import os

from config import TEST_MODE


def get_unique_destination(destination_folder, filename):

    name, extension = os.path.splitext(filename)

    destination_path = os.path.join(
        destination_folder,
        filename
    )

    counter = 2

    while os.path.exists(destination_path):

        new_filename = f"{name}_{counter}{extension}"

        destination_path = os.path.join(
            destination_folder,
            new_filename
        )

        counter += 1

    return destination_path


def move_document(source_path, destination_folder, filename):

    if not os.path.isfile(source_path):

        return {
            "status": "Failed",
            "message": "Source PDF does not exist."
        }

    source_path = os.path.abspath(source_path)

    if TEST_MODE:

        preview_path = get_unique_destination(
            destination_folder,
            filename
        )

        return {
            "status": "Preview",
            "source": source_path,
            "destination": preview_path,
            "message": "Document would be moved. Test mode is enabled."
        }

    try:

        os.makedirs(
            destination_folder,
            exist_ok=True
        )

        # Find an available filename
        destination_path = get_unique_destination(
            destination_folder,
            filename
        )

        # Rename on the same drive. On Windows, this fails rather
        # than overwriting if another file takes the destination.
        while True:

            try:

                os.rename(
                    source_path,
                    destination_path
                )

                break

            except FileExistsError:

                destination_path = get_unique_destination(
                    destination_folder,
                    filename
                )

        return {
            "status": "Moved",
            "source": source_path,
            "destination": destination_path,
            "message": "Document moved successfully."
        }

    except Exception as error:

        return {
            "status": "Failed",
            "source": source_path,
            "message": str(error)
        }