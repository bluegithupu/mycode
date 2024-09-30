import Head from 'next/head'
import Header from '../components/Header'

export default function About() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>关于 - 我的Next.js应用</title>
        <meta name="description" content="关于我的Next.js应用" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-blue-600 mb-8">关于我们</h1>
        
        <div className="bg-white shadow-md rounded-lg p-6 max-w-2xl mx-auto">
          <p className="text-lg mb-4">
            这是一个使用Next.js创建的示例应用。我们正在学习和探索Next.js的各种功能。
          </p>
          <p className="text-lg mb-4">
            Next.js 是一个轻量级的 React 框架，它提供了许多强大的功能，包括：
          </p>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>服务器端渲染 (SSR)</li>
            <li>静态站点生成 (SSG)</li>
            <li>文件系统路由</li>
            <li>API 路由</li>
            <li>内置 CSS 支持</li>
            <li>代码分割和优化</li>
          </ul>
          <p className="text-lg">
            通过这个应用，我们展示了如何创建一个简单的用户管理系统，包括添加和删除用户的功能。
          </p>
        </div>
      </main>
    </div>
  )
}