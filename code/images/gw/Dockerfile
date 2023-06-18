# 基于的基础镜像
FROM python:3.9.16

# 设置app文件夹是工作目录
WORKDIR /usr/src/app
RUN pwd
# 先将依赖文件拷贝到项目中
COPY requirements.txt /usr/src/app

# 执行指令，安装依赖
RUN pip install -r requirements.txt

# 拷贝当前目录的项目文件和代码
COPY . /usr/src/app

# 执行命令
CMD [ "python", "consumer.py" ]