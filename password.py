import hashlib
import os

class Password:
    """Password class."""

    def __init__(self, service: str, password: str) -> None:
        """
        Constructs a Password object.

        Args:
            service (str): The service for the password.
            password (str): The password to be stored.
        """
        self._service = service
        self._password = password
        self._salt = self.generate_salt()
        self._hashed_password = self.hash_password()

    def generate_salt(self) -> bytes:
        """Generates a salt for the password."""
        return os.urandom(16)

    def hash_password(self) -> bytes:
        """Creates a hash of the password."""
        return hashlib.pbkdf2_hmac(
            'sha256', self._password.encode('utf-8'), self._salt, 100000
        )

    @property
    def password(self) -> bytes:
        """Getter for hashed password."""
        return self._hashed_password

    @property
    def service(self) -> str:
        """Getter for service."""
        return self._service


class PasswordManager:
    """Manages passwords."""

    def __init__(self, file_path: str = "~/Desktop/passwords.txt") -> None:
        """
        Opens passwords file and reads its contents into a dictionary.

        Args:
            file_path (str): The path to the passwords file.
        """
        self.file_path = os.path.expanduser(file_path)
        self._passwords = {}
        self._load_passwords()

    def _load_passwords(self) -> None:
        """Loads passwords from a file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        service, password = line.split(':', 1)
                        self._passwords[service.strip()] = password.strip()

    @property
    def passwords(self) -> dict[str, str]:
        """Returns the passwords dictionary."""
        return self._passwords

    def add_new_password(self, service: str, password: str) -> bool:
        """Adds a new password."""
        if service in self._passwords:
            return False
        
        new_password = Password(service, password)

        salt = new_password._salt.hex()  # Convert salt to hex for storage
        hashed_password = new_password.password.hex()  # Convert hash to hex for storage
        
        self._passwords[service] = f"{salt}|{hashed_password}"
        
        return True


    def verify_password(self, service: str, input_password: str) -> bool:
        """
        Verifies if the input password matches the stored password for a given service.

        Args:
            service (str): The service to look up.
            input_password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        # Check if the service exists
        if service not in self._passwords:
            print(f"Service '{service}' not found.")
            return False

        # Retrieve the stored hashed password and salt (assumes they're separated by a delimiter)
        stored_hashed_password = self._passwords[service]

        # To decode stored salt and hash (if stored together):
        # Example assumes salt and hash are stored as "salt|hash"
        try:
            stored_salt, stored_hash = stored_hashed_password.split('|')
            stored_salt = bytes.fromhex(stored_salt)  # Convert hex salt back to bytes
            stored_hash = bytes.fromhex(stored_hash)  # Convert hex hash back to bytes
        except ValueError:
            print("Password data corrupted for service:", service)
            return False

        # Hash the input password using the same salt
        new_hashed_password = hashlib.pbkdf2_hmac(
            'sha256', input_password.encode('utf-8'), stored_salt, 100000
        )

        # Compare the newly hashed password with the stored hash
        return new_hashed_password == stored_hash
    
    def save_to_file(self) -> None:
        """Saves the passwords to a file."""
        with open(self.file_path, 'w') as file:
            for service, password in self._passwords.items():
                file.write(f"{service}: {password}\n")

    def get_all_passwords(self):
        """Returns the list of all passwords"""
        return self.passwords
    