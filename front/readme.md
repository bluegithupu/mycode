# 前端项目

本项目是一个使用现代前端技术栈构建的Web应用程序。

## 技术栈

- [框架名称] (例如: React, Vue, Angular等)
- Tailwind CSS

## 开始使用

### 前提条件

- Node.js (版本 X.X.X 或更高)
- npm 或 yarn

### 安装

1. 克隆仓库:
   ```
   git clone [仓库URL]
   ```

2. 进入项目目录:
   ```
   cd front
   ```

3. 安装依赖:
   ```
   npm install
   ```
   或
   ```
   yarn install
   ```

### 运行开发服务器

```
npm run dev
```
或
```
yarn dev
```

## 构建

要构建生产版本,运行:

```
npm run build
```
或
```
yarn build
```

## 项目结构

项目的目录结构如下:

```
front/
├── components/     # 可复用的组件
├── lib/            # 工具函数和数据库操作
├── pages/          # 页面组件和API路由
│   └── api/        # API路由
├── public/         # 静态资源文件
├── styles/         # 样式文件
├── .gitignore      # Git忽略文件
├── next.config.js  # Next.js 配置文件
├── package.json    # 项目依赖和脚本
├── postcss.config.js # PostCSS 配置文件
└── tailwind.config.js # Tailwind CSS 配置文件
```

- `components/`: 存放可复用的React组件。
- `lib/`: 包含工具函数和数据库操作相关的代码。
- `pages/`: 存放路由对应的页面组件和API路由。
  - `api/`: 包含所有的API路由处理函数。
- `public/`: 存放不需要经过webpack处理的静态资源文件。
- `styles/`: 包含全局样式和Tailwind CSS的自定义样式。

## Tailwind CSS 配置

本项目使用Tailwind CSS进行样式设计。配置文件位于 `tailwind.config.js`。

## API 路由

本项目使用Next.js的API路由功能。API路由文件位于 `pages/api/` 目录下。

## 数据库

本项目使用SQLite作为数据库。数据库操作相关的代码位于 `lib/db.js` 文件中。

## 贡献

欢迎贡献！请阅读 `CONTRIBUTING.md` 了解如何为本项目做出贡献。

## 许可证

[选择适当的许可证，例如 MIT, Apache 2.0 等]
