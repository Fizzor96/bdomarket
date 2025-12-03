# pylint: disable=missing-module-docstring, line-too-long
import os
import json
from typing import Optional, Any


class ApiResponse:
    """
    Represents a standardized API response, encapsulating success status, HTTP status code, message, and content.

    Args:
        success (bool): Indicates if the response was successful.
        status_code (int): The HTTP status code of the response.
        message (str): A message describing the response.
        content (Any): The content of the response, can be dict, str, or bytes for images.

    Attributes:
        success (bool): Indicates if the response was successful.
        status_code (int): The HTTP status code of the response.
        message (str): A message describing the response.
        content (Any): The content of the response.
        url (str): The URL of the response.
        headers (str): The headers of the response.
    """

    def __init__(self, success: bool = False, status_code: Optional[int] = None,
                 message: str = "No message provided", content: Optional[Any] = None,
                 url: Optional[str] = None, headers: Optional[str] = None):
        self.success = success
        self.status_code = status_code
        self.message = message
        self.content = content
        self.url = url
        self.headers = headers

    def __str__(self) -> str:
        """String representation of the ApiResponse object.

        Returns:
            str: A string containing the success status, status code, message, and content of the response.
        """
        if isinstance(self.content, bytes):
            content_str = f"Binary image content (length: {len(self.content)} bytes)"
        else:
            content_str = json.dumps(
                self.content, indent=2, ensure_ascii=False)
        return (
            (f"URL: {self.url}\n" if self.url else "")
            + f"success: {self.success}\n"
            f"status_code: {self.status_code}\n"
            f"message: {self.message}\n"
            f"content: {content_str}"
        )

    def save_to_file(self, path: str, mode: str = "w") -> None:
        """Save the ApiResponse content to a file. Handles JSON or binary image.

        Args:
            path (str): The file path where the content should be saved.
        """
        if "application/json" in self.headers.get("Content-Type", "").lower():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if isinstance(self.content, bytes):
                with open(path, "wb") as f:
                    f.write(self.content)
            else:
                data = {
                    "success": self.success,
                    "status_code": self.status_code,
                    "message": self.message,
                    "content": self.content
                }
                with open(path, mode, encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise TypeError("Response content is not in json format")

    def save_image(self, path: str) -> None:
        """Save the image content to a file if it's binary.

        Args:
            path (str): The file path where the image should be saved.
        """
        if not isinstance(self.content, bytes):
            raise ValueError("Content is not an image (bytes)")
        if "image/png" in self.headers.get("Content-Type", "").lower():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(self.content)

    def show_image(self) -> None:
        """Display the image if content is binary using PIL."""
        if not isinstance(self.content, bytes):
            raise ValueError("Content is not an image (bytes)")
        try:
            if "image/png" in self.headers.get("Content-Type", "").lower():
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(self.content))
                img.show()
            else:
                pass
        except ImportError:
            raise ImportError(
                "PIL library is required to show images. Install with 'pip install pillow'")
