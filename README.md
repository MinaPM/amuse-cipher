# amuse-cipher

## Requirements
This project requires Python and uses the `bloom-filter` package. All dependencies are listed in the `requirements.txt` file.

## Installation

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - **On Windows:**
     ```powershell
     .\.venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Testing

The project includes a full test suite built with Python's standard `unittest` framework, meaning no additional dependencies are required to run the tests.

To run the entire test suite, ensure your virtual environment is activated and execute:

```bash
python -m unittest discover tests
```

This will run both the unit tests for the core encryption/decryption algorithms and the integration tests for the CLI script.

## Usage

To run the project on a file, use the `main.py` script and pass the input file as an argument:

```bash
python main.py <input_file>
```

For example, to run it on the provided `test.txt` file:

```bash
python main.py test.txt
```

This will encrypt the file into a `.enc` file (which contains the Bloom Filter representation) and then decrypt it, showing a progress bar and outputting a `.decrypted` file.

## Algorithm

### Algorithm 1: Encrypt a message/file into a Bloom Filter

$$
\begin{array}{ll}
\textbf{1} & \textbf{Function } \text{EncryptFile}(file, H) \\
\textbf{2} & \quad size \leftarrow \textbf{len}(file) \\
\textbf{3} & \quad BF \leftarrow \text{BloomFilter}(size, prob) \\
\textbf{4} & \quad \textbf{for } i \leftarrow 0 \textbf{ to } size - 1 \textbf{ do} \\
\textbf{5} & \quad \quad H\text{.update}(file[i]) \\
\textbf{6} & \quad \quad BF\text{.insert}(H\text{.digest}()) \\
\textbf{7} & \quad \textbf{foreach } \phi \in postamble \textbf{ do} \\
\textbf{8} & \quad \quad H\text{.update}(\phi), \\
           & \quad \quad BF\text{.insert}(H\text{.digest}()) \\
\textbf{9} & \quad \textbf{return } BF;
\end{array}
$$

### Algorithm 2: Decrypt a message/file from a Bloom Filter

$$
\begin{array}{ll}
\textbf{1} & \textbf{Function } \text{DecryptFile}(BF, H, size, postamble) \\
\textbf{2} & \quad P \leftarrow \bot, Q_{bfs} \leftarrow \bot \quad \triangleright \text{Start from an empty prefix and creating a queue} \\
\textbf{3} & \quad Q_{bfs}\text{.append}(\langle H, P \rangle) \quad \triangleright \text{Initialize BFS queue with the empty string} \\
\textbf{4} & \quad \textbf{while } Q_{bfs} \neq \bot \textbf{ do} \\
\textbf{5} & \quad \quad \langle H, P \rangle \leftarrow Q_{bfs}\text{.pop}() \quad \triangleright \text{Dequeue a pair of hash function \& a prefix} \\
\textbf{6} & \quad \quad \textbf{if } \textbf{len}(P) < size \textbf{ then} \\
\textbf{7} & \quad \quad \quad \textbf{foreach } c \in \sigma \textbf{ do} \\
\textbf{8} & \quad \quad \quad \quad P_{opt} \leftarrow P + c, H_{opt} \leftarrow H\text{.copy}(), H_{opt}\text{.update}(c) \\
\textbf{9} & \quad \quad \quad \textbf{if } BF\text{.check}(H_{opt}\text{.digest}()) \textbf{ then} \\
\textbf{10} & \quad \quad \quad \quad Q_{bfs}\text{.append}(\langle H_{opt}, P_{opt} \rangle) \quad \triangleright \text{Enqueue candidate pair} \\
\textbf{11} & \quad \textbf{else} \\
\textbf{12} & \quad \quad success \leftarrow \textbf{true} \\
\textbf{13} & \quad \quad \textbf{foreach } \phi \in postamble \textbf{ do} \\
\textbf{14} & \quad \quad \quad H\text{.update}(\phi) \\
\textbf{15} & \quad \quad \quad \textbf{if not } BF\text{.check}(H\text{.digest}()) \textbf{ then} \\
\textbf{16} & \quad \quad \quad \quad success \leftarrow \textbf{false} \textbf{ \& break} \quad \triangleright \text{False positive full message} \\
\textbf{17} & \quad \quad \textbf{if } success = \textbf{true} \textbf{ then} \\
\textbf{18} & \quad \quad \quad \textbf{return } P \\
\textbf{19} & \quad \textbf{return } \bot;
\end{array}
$$
