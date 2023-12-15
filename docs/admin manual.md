# Admin Manual

## Installation
**Disclaimer:** GPU support will require additional configuration steps not covered in this manual. Refer to the GPU section for more information.

### Docker Installation:
1. **Clone the Repository:** Ensure that Docker is installed on your host machine and clone this repository.

2. **Configure Environment:** Set up the `.env` file as outlined in the Configuration section.

3. **Build Docker Image:**
   ```bash
   make build
   ```

4. **Run the Container:**
   ```bash
   make up
   ```

   The service should now be accessible on `localhost` via HTTP (port 5000).

**Stopping the Container:**
   ```bash
   make down
   ```

### Local Python Interpreter Setup

This project requires Python 3.11. Verify the Python version before proceeding.

1. **Clone the Repository:** Clone this repository to your host machine.

2. **Environment Configuration:** Configure the `.env` file as mentioned in the Configuration section. Note: For local setups, the `.env` file must be placed in the "./src" directory.

3. **Install Dependencies:**
   ```bash
   cd src
   pip install -r requirements.txt
   ``` 

4. **Launch Application:**
   ```bash
   cd src
   python3 app.py
   ```

   The service should now be running on `localhost` via HTTP (port 5000).

**Stopping the Application:** Terminate the process using Ctrl + C.

### MediaWiki Integration

To integrate the query prompt inside of MediaWiki, install the LlamaPage extension:

1. **Install Extension:** Download and install the LlamaPage extension from [LlamaPage GitHub Repository](https://github.com/?????/LlamaPage).

2. **Activate Extension:** Add the following to your `localsettings.php`:
   ```php
   wfLoadExtension( 'LlamaPage' );
   ```

3. **Restart MediaWiki.**

## Configuration

Configure the project using the `.env` file located at the project's root:

```bash
MEDIAWIKI_URL=https://www.confident-conference.org/index.php/
MEDIAWIKI_API_URL=https://www.confident-conference.org/api.php
MEDIAWIKI_NAMESPACES=7200
MODEL_URL=https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_M.gguf
MODEL_PATH=../codellama-13b-instruct.Q4_K_M.gguf
PERSISTENT_STORAGE_DIR=mediawiki_index
```

### MediaWiki Configuration
- **MEDIAWIKI_URL:** Base URL of the wiki, ending with "index.php/".
- **MEDIAWIKI_API_URL:** URL for the MediaWiki API.
- **MEDIAWIKI_NAMESPACES:** Namespace IDs separated by commas.
- **MEDIAWIKI_APFROM:** Start character for page reading (e.g., "E").
- **MEDIAWIKI_APTO:** End character for page reading (e.g., "O").
- **PERSISTENT_STORAGE_DIR:** Directory for saving and loading the index. If not specified, the index is reloaded at each run.

### Model Configuration:

Configure the model using a direct download URL or a local file:

- **MODEL_URL:** Direct URL to download the model file.
- **MODEL_PATH:** Relative path to a local model file.

At least one of these environment variables is required.

The used llama-cpp-python expects model to be in the .gguf format!

## GPU Support

To use the llama.CCP model with a GPU, follow the platform-specific guide on the [llama.CCP GitHub page](https://github.com/ggerganov/llama.cpp).

### Example: CUDA

For CUDA (cuBLAS) acceleration, install the latest NVIDIA drivers and the NVIDIA CUDA Toolkit.

Build llama-cpp-python with cuBLAS support:
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```
Note: The build will fail if dependencies, such as the nvcc toolchain, are missing.

Once the llama-cpp-python wheel is built for your platform, run the application as described in the Installation section.
