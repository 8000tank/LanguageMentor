# 使用 Python 3.11 精简版作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 接收构建参数
ARG OPENAI_API_KEY

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860 \
    OPENAI_API_KEY=${OPENAI_API_KEY} \
    PYTHONPATH=/app/src

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 创建必要的目录
RUN mkdir -p /app/content/intro /app/prompts

# 复制项目文件
COPY requirements.txt ./
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY prompts/ /app/prompts/
COPY content/ /app/content/
COPY validate_tests.sh ./

# 设置执行权限
RUN chmod +x validate_tests.sh

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest pytest-cov

# 运行测试
RUN ./validate_tests.sh || exit 1

# 清理不必要的文件
RUN apt-get purge -y --auto-remove git \
    && rm -rf /root/.cache \
    && rm -rf /root/.local \
    && rm -rf /tmp/*

# 暴露端口
EXPOSE 7860

# 设置启动命令
CMD ["python", "src/main.py"] 