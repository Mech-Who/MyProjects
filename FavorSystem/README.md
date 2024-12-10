# FavorSys

## Run

```shell
uvicorn main:app --reload
```

执行过程中，可以通过`--host`参数和`--port`参数指定 ip 和端口。

```shell
uvicorn main:app --host 0.0.0.0 --port 80 --reload
```

## Docs

启动服务后，通过`http://127.0.0.1:8000/docs`或`http://127.0.0.1:8000/redoc`即可访问接口文档。

## dependencies

- fastapi / "fastapi[all]" (包括所有插件)
- "uvicorn[standard]"
- pydantic

fastapi 插件包括：

- 用于 Pydantic：
  - email-validator - 用于 email 校验。
- 用于 Starlette：
  - httpx - 使用 TestClient 时安装。
  - jinja2 - 使用默认模板配置时安装。
  - python-multipart - 需要通过 request.form() 对表单进行「解析」时安装。
  - itsdangerous - 需要 SessionMiddleware 支持时安装。
  - pyyaml - 使用 Starlette 提供的 SchemaGenerator 时安装（有 FastAPI 你可能并不需要它）。
  - graphene - 需要 GraphQLApp 支持时安装。
- 用于 FastAPI / Starlette：
  - uvicorn - 用于加载和运行你的应用程序的服务器。
  - orjson - 使用 ORJSONResponse 时安装。
  - ujson - 使用 UJSONResponse 时安装。
