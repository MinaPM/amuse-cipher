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

## Algorithm

### Algorithm 1: Encrypt a message/file into a Bloom Filter

---

**1** &nbsp;**Function** `EncryptFile`($file, H$)  
**2** &nbsp;$size \leftarrow \mathbf{len}(file)$  
**3** &nbsp;$BF \leftarrow \mathbf{BloomFilter}(size, prob)$  
**4** &nbsp;**for** $i \leftarrow 0$ **to** $size - 1$ **do**  
**5** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$H\text{.update}(file[i])$  
**6** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$BF\text{.insert}(H\text{.digest}())$  
**7** &nbsp;**foreach** $\phi \in postamble$ **do**  
**8** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$H\text{.update}(\phi)$,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$BF\text{.insert}(H\text{.digest}())$  
**9** &nbsp;**return** $BF$;  

---

### Algorithm 2: Decrypt a message/file from a Bloom Filter

---

**1** &nbsp;**Function** `DecryptFile`($BF, H, size, postamble$)  
**2** &nbsp;$P \leftarrow \bot, Q_{bfs} \leftarrow \bot \quad \triangleright$ Start from an empty prefix and creating a queue  
**3** &nbsp;$Q_{bfs}\text{.append}(\langle H, P \rangle) \quad \triangleright$ Initialize BFS queue with the empty string  
**4** &nbsp;**while** $Q_{bfs} \neq \bot$ **do**  
**5** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\langle H, P \rangle \leftarrow Q_{bfs}\text{.pop} \quad \triangleright$ Dequeue a pair of hash function & a prefix  
**6** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**if** $\mathbf{len}(P) < size$ **then**  
**7** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**foreach** $c \in \sigma$ **do**  
**8** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$P_{opt} \leftarrow P + c, H_{opt} \leftarrow H\text{.copy}(), H_{opt}\text{.update}(c)$  
**9** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**if** $BF\text{.check}(H_{opt}\text{.digest}())$ **then**  
**10** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$Q_{bfs}\text{.append}(\langle H_{opt}, P_{opt} \rangle) \quad \triangleright$ Enqueue candidate pair  
**11** **else**  
**12** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$success \leftarrow \mathbf{true}$  
**13** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**foreach** $\phi \in postamble$ **do**  
**14** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$H\text{.update}(\phi)$  
**15** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**if not** $BF\text{.check}(H\text{.digest}())$ **then**  
**16** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$success \leftarrow \mathbf{false}$ **& break** $\quad \triangleright$ False positive full message  
**17** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**if** $success = \mathbf{true}$ **then**  
**18** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**return** $P$  
**19** **return** $\bot$;  

---
