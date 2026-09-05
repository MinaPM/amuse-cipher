import unittest
import subprocess
import os
import sys


class TestMainScript(unittest.TestCase):
    def setUp(self):
        # Create a temporary test file
        self.test_file = "temp_test_input.txt"
        self.test_content = b"Integration test message"
        with open(self.test_file, "wb") as f:
            f.write(self.test_content)

        # Files that will be created by main.py
        self.encrypted_file = self.test_file + ".enc"
        self.decrypted_file = self.test_file + ".decrypted"

        # Determine python executable to use (current python)
        self.python_exec = sys.executable

    def tearDown(self):
        # Cleanup created files
        for file in [self.test_file, self.encrypted_file, self.decrypted_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_main_success(self):
        # Run main.py with the test file
        # We need to run it in the parent directory where main.py is
        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_dir, "main.py")

        result = subprocess.run(
            [self.python_exec, main_script, self.test_file],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        # Check success
        self.assertEqual(result.returncode, 0,
                         f"Script failed with output: {result.stderr}")
        self.assertIn(
            "[SUCCESS] Decrypted message matches original!", result.stdout)

        # Check files were created
        self.assertTrue(os.path.exists(self.encrypted_file))
        self.assertTrue(os.path.exists(self.decrypted_file))

        # Check decrypted content
        with open(self.decrypted_file, "rb") as f:
            decrypted_content = f.read()

        self.assertEqual(decrypted_content, self.test_content)

    def test_main_missing_file(self):
        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_dir, "main.py")

        result = subprocess.run(
            [self.python_exec, main_script, "non_existent_file_999.txt"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "Error: File 'non_existent_file_999.txt' not found.", result.stdout)

    def test_main_no_args(self):
        project_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        main_script = os.path.join(project_dir, "main.py")

        result = subprocess.run(
            [self.python_exec, main_script],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage: python main.py <input_file>", result.stdout)


if __name__ == "__main__":
    unittest.main()
