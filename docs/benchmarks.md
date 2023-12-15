# Benchmarks

## Components

### Compute Resources
|      | CPU                  | RAM   | Notes              |
|------|----------------------|-------|--------------------|
| CR01 | Intel Core i5-10310U | 32 GB | Dell Latitude 5310 |
| CR02 | Intel Core i5-7500   | 32 GB | Thomas Krenn       |
| CR03GPU | intel Core i7-12700H | 32GB  | Nvidia RTX 3070Ti Mobile

### Environments

|     | Operating System              | |
|-----|-------------------------------|-|
| E01 | Ubuntu 22.04@Windows 10 WSL 2 | |
| E02 | Rocky Linux 9 linux 5.14.00   | |


### Models

|     | Name                               | Quand Method | Bits | Size    |
|-----|------------------------------------|--------------|------|---------|
| M01 | codellama-13b-instruct.Q4_K_M.gguf | Q4_K_M       | 4    | 7.87 GB |
| M02 | codellama-7b-instruct.Q4_K_M.gguf  | Q4_K_M       | 4    | 3.80 GB |
| M03 | mistral-7b-openorca                | Q3_K_S       | 3    | 2.95 GB |
| M04 | mistral-7b-openorca                | Q4_K_M       | 4    | 4.07 GB |

### Configurations

|     | LlamaIndex   | GPU Enabled |
|-----|--------------|-------------|
| C01 | 0.9.14-post3 | no          |
| G01 | 0.9.14-post3 | cuda        |


## Measurements

- load time: time it takes for the model to load.
- sample time: time it takes to "tokenize" (sample) the prompt message for it to be processed by the program.
- prompt eval time: time it takes to process the tokenized prompt message. If this isn't done, there would be no context for the model to know what token to predict next.
- eval time: time needed to generate all tokens as the response to the prompt (excludes all pre-processing time, and it only measures the time since it starts outputting tokens).

### Testcases
- T01: No Vector Index, "What do you know about SMW?"

### Results

| | Setup               |   load    | sample | prompt eval | eval     | total  |     notes     |
|-|---------------------|-----------|--------|-------------|----------|--------|---------------|
| | CR2.E02.M01.C01     | 19.05s    | 0.09s  | 19.05s      | 81.68s   | 101.31s|               |
| | CR2.E02.M02.C01     | 9.76s     | 0.11s  | 9.76s       | 51.80s   | 62.25s |               |
| | CR2.E02.M03.C01     | 12.10s    | 0.11s  | 12.10s      | 55.23s   | 68.03s |               |
| | CR2.E02.M04.C01     | 10.13s    | 0.11s  | 10.13s      | 53.56s   | 64.38s |               |
| | CR3GPU.E001.M01.G01 | 123.54s   | 0.05s  | 123.54s     | 46.65s   | 170.62s|               |
| | CR3GPU.E001.M02.G01 | 0.73s     | 0.04s  | .72s        | 11.28s   | 12.41s |               |
| | CR3GPU.E001.M03.G01 | 0.62s     | 0.05s  | .62s        | 9.82s    | 10.86s |               |
| | CR3GPU.E001.M04.G01 | 1.88s     | 0.05s  | .25s        | 9.18s    | 9.86s  |               |


### Testcases
- T02: SMW.org, Namespace XXX V to V "What is SMWCon?"

### Results

| | Setup               |   load    | sample | prompt eval | eval     | total  |     notes     |
|-|---------------------|-----------|--------|-------------|----------|--------|---------------|
| | CR2.E02.M01.C01     | 134.51s   | 0.03s   | 561.57s     | 39.66s   | 601.51s|               |
| | CR2.E02.M02.C01     | 71.25s    | 0.04s   | 303.20s     | 21.86s   | 325.35s|               |
| | CR2.E02.M03.C01     | 89.79s    | 0.04s   | 377.52s     | 24.83s   | 402.68s|               |
| | CR2.E02.M04.C01     | 89.79s    | 0.04s   | 377.52s     | 24.83s   | 402.68s|               |
| | CR3GPU.E001.M01.G01 | 83.03s    | 0.01s   | 370.49s     | 22.48s   | 393.25s|    1. Run     |
| | CR3GPU.E001.M01.G01 | 83.03s    | 0.01s   | 0s          | 26.18s   | 26.37s |    2. Run     |
| | CR3GPU.E001.M02.G01 | 2.51s     | 0.01s   | 16.22s      | 11.84s   | 28.95s |               |
| | CR3GPU.E001.M03.G01 | 0.44s     | 0.03s   | 13.14s      | 25.19s   | 39.37s | bad response  | 
| | CR3GPU.E001.M04.G01 | 1.88s     | 0.08s   | 13.43s      | 3.84s    | 17.97s |               |



### Testcases
- T03: No Vector Index, "how are you?"

### Results

| | Setup               |   load    | sample | prompt eval | eval     | total  |     notes     |
|-|---------------------|-----------|--------|-------------|----------|--------|---------------|
| | CR2.E001.M01.G01    | 17.75s    | 0.015s | 17.75s      | 12.53s   | 30.38s |               |
| | CR2.E001.M02.G01    | 9.25s     | 0.015s | 9.25s       | 6.63s    | 15.97s |               |
| | CR2.E001.M03.G01    | 11.41s    | 0.11s  | 11.41s      | 55.20s   | 67.30s |               |
| | CR2.E001.M04.G01    | 10.13s    | 0.1s   | 1.17s       | 53.39s   | 55.24s |               |
| | CR3GPU.E001.M01.G01 | 103.46s   | 0.009s | 103.46s     | 8.38s    | 111.92s|               |
| | CR3GPU.E001.M02.G01 | 0.62s     | 0.011s | 0.62s       | 2.41s    | 3.13s  |               |
| | CR3GPU.E001.M03.G01 | 0.44s     | 0.03s  | 0.44s       | 6.06s    | 6.77s  |               |
| | CR3GPU.E001.M04.G01 | 1.88s     | 0.011s |00.09s       | 1.99s    | 2.18s  |               |

### Testcases
- T03: confident wiki - "When did SMWCon 2019 take place and where?"

### Results

| | Setup               |   load    | sample | prompt eval | eval     | total  |     notes     |
|-|---------------------|-----------|--------|-------------|----------|--------|---------------|
| | CR2.E001.M01.G01    | 184.62s   | 0.016s | 773.68s     | 20.29s   | 794.13s|               |
| | CR2.E001.M02.G01    | 71.22s    | 0.012s | 314.00s     | 7.05s    | 321.17s|               |
| | CR2.E001.M03.G01    | 89.59s    | 0.014s | 384.36s     | 8.09s    | 392.59s|               |
| | CR2.E001.M04.G01    | 75.45s    | 0.105s | 326.87s     | 8.62s    | 335.63s|               |
| | CR3GPU.E001.M01.G01 | 39.92s    | 0.0068s| 342.16s     | 10.17s   | 352.48s|               |
| | CR3GPU.E001.M02.G01 | 30.89s    | 0.0059s| 143.30s     | 4.11s    | 147.44s|               |
| | CR3GPU.E001.M03.G01 | 1.98s     | 0.0092s| 14.12s      | 4.38s    | 18.62s |               |
| | CR3GPU.E001.M04.G01 | 35.20s    | 0.0055s| 166.09s     | 3.10s    | 169.29s|               |





| | model  |   response                                                                                                                                |
|-|--------|-------------------------------------------------------------------------------------------------------------------------------------------|
| | M01    |Based on the given context, SMWCon 2019 took place in Paris, France from September 25 to September 27, 2019.                               |
| | M02    |SMWCon 2019 took place from September 25th to September 27th in Paris, France.                                                             |
| | M03    |The Semantic MediaWiki Conference (SMWCon) Fall 2019 took place from September 25th to September 27th, 2019. It was held in Paris, France. |
| | M04    |SMWCon 2019 took place from September 25 to September 27, 2019 in Paris, France.                                                           |