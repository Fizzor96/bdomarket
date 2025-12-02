# pylint: disable=missing-module-docstring, line-too-long
import os
import json

class ApiResponse:
    """
    Represents a standardized API response, encapsulating success status, HTTP status code, message, and content.

    Args:
        success (bool): Indicates if the response was successful.
        status_code (int): The HTTP status code of the response.
        message (str): A message describing the response.
        content (str): The content of the response.

    Attributes:
        success (bool): Indicates if the response was successful.
        status_code (int): The HTTP status code of the response.
        message (str): A message describing the response.
        content (str): The content of the response.
        content (str): The content of the response, typically in JSON format.
    """
    def __init__(self, success: bool = False, status_code: int = -1, message: str = "", content: str = ""):
        self.success = success
        self.status_code = status_code
        self.message = message
        self.content = content

    def __str__(self) -> str:
        """String representation of the ApiResponse object.

        Returns:
            str: A string containing the success status, status code, message, and content of the response.
        """
        return f"success: {self.success}\nstatus_code: {self.status_code}\nmessage: {self.message}\ncontent: {json.dumps(self.content, indent=2, ensure_ascii=False)}"

    # def deserialize(self) -> Dict[str, Any]:
    #     try:
    #         return json.loads(self.content) if self.content else {}
    #     except json.JSONDecodeError:
    #         raise ValueError("Failed to deserialize content")

    def save_to_file(self, path: str, mode: str = "w") -> None:
        """Save the ApiResponse content to a file in JSON format.

        Args:
            path (str): The file path where the content should be saved.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            "success": self.success,
            "status_code": self.status_code,
            "message": self.message,
            "content": self.content
        }
        with open(path, mode, encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
