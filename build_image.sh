#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 检查 OPENAI_API_KEY 环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}警告：OPENAI_API_KEY 环境变量未设置${NC}"
fi

# 获取当前 git 分支名
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
if [ $? -ne 0 ]; then
    echo -e "${RED}错误：无法获取 git 分支名${NC}"
    exit 1
fi

# 设置 Docker 镜像名称和标签
IMAGE_NAME="language-mentor"
IMAGE_TAG="${BRANCH_NAME}"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

# 构建 Docker 镜像，传入当前环境变量
echo "开始构建 Docker 镜像: ${FULL_IMAGE_NAME}"
if docker build \
    --build-arg OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -t ${FULL_IMAGE_NAME} .; then
    echo -e "${GREEN}镜像构建成功！${NC}"
    echo -e "镜像名称: ${GREEN}${FULL_IMAGE_NAME}${NC}"
    echo -e "你可以使用以下命令运行容器："
    echo -e "${GREEN}docker run -p 7860:7860 ${FULL_IMAGE_NAME}${NC}"
else
    echo -e "${RED}镜像构建失败！${NC}"
    exit 1
fi 