# XYUnionAuthNeo

XYUnionAuthNeo（简称为”XYUAN“或”XYUA“）是一个用于提供用户管理、身份验证、权限管理的微服务，是XYUnionAuth项目的最新版本。

XYUAN提供了一系列HTTP API用于供后端服务器调用，并且基于`casbin-python`实现了基于ABAC模型的权限管理系统。

## 内置资源列表

> 注意：XYUAN的权限节点**没有**继承机制，也没有实现通配符等功能。例如即使一个用户有权限访问`xyunionauth.application`，他也没法访问`xyunionauth.application.token`。

1. `xyunionauth.application`
2. `xyunionauth.application.token`

## 内置操作列表

1. `read`
2. `write`
3. `delete`
4. `all`

