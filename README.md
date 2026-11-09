# LangChain 1.2 学习项目

这个项目专门存放 LangChain 1.2 的可运行小例子。每个模块一个目录，每个知识点一个 Python 文件，方便边学边改。

## 环境

项目复用已有的 Conda 环境 `langchain1.2`，不在项目目录创建 `.venv`：

```bash
conda activate langchain1.2
cd new_/LangChain
python -m pip install -r requirements.txt
```

真实模型调用前复制 `.env.example` 为 `.env`，填写供应商密钥，并按需安装 `requirements-provider.txt`。基础示例不需要密钥。

## 目录

```text
src/langchain_study/
├── config.py
├── 01_models/
├── 02_prompts/
├── 03_runnables/
├── 04_structured_output/
├── 05_tools/
├── 06_agents/
├── 07_memory/
├── 08_middleware/
└── 09_rag/
```

编号文件按建议顺序学习。由于目录名和文件名带编号，统一使用模块方式运行：

```bash
PYTHONPATH=src python -m langchain_study.02_prompts.01_chat_prompt_template
PYTHONPATH=src python -m langchain_study.03_runnables.01_lcel_pipeline
PYTHONPATH=src python -m langchain_study.09_rag.01_document_splitter
```

模型、Agent、Memory 示例需要真实模型和对应 provider 配置；先从 `01_models/02_message_types.py`、`02_prompts/`、`03_runnables/` 开始。

运行测试：

```bash
conda activate langchain1.2
python -m pytest
```
