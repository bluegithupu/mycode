import { useState, useEffect } from 'react'
import Head from 'next/head'
import Header from '../components/Header'

export default function Home() {
  const [users, setUsers] = useState([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    const res = await fetch('/api/users')
    const data = await res.json()
    setUsers(data)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email })
    })
    if (res.ok) {
      setName('')
      setEmail('')
      setMessage('用户添加成功!')
      fetchUsers()
      setTimeout(() => setMessage(''), 3000)
    } else {
      const errorData = await res.json()
      setMessage(`添加失败: ${errorData.error}`)
    }
  }

  const handleDelete = async (id) => {
    const res = await fetch(`/api/users/${id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      setMessage('用户删除成功!')
      fetchUsers()
      setTimeout(() => setMessage(''), 3000)
    } else {
      const errorData = await res.json()
      setMessage(`删除失败: ${errorData.error}`)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>我的Next.js应用</title>
        <meta name="description" content="一个简单的Next.js应用例子" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-blue-600 mb-8">欢迎来到我的Next.js应用!</h1>
        
        {message && <p className="bg-green-500 text-white p-3 rounded-md text-center mb-4">{message}</p>}

        <form onSubmit={handleSubmit} className="max-w-md mx-auto mb-8">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="姓名"
            required
            className="w-full p-2 mb-4 border border-gray-300 rounded-md"
          />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="邮箱"
            required
            className="w-full p-2 mb-4 border border-gray-300 rounded-md"
          />
          <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition-colors">
            添加用户
          </button>
        </form>

        <h2 className="text-2xl font-semibold text-green-600 mb-4">用户列表:</h2>
        <ul className="space-y-2">
          {users.map(user => (
            <li key={user.id} className="bg-white p-4 rounded-md shadow flex justify-between items-center">
              <span>{user.name} ({user.email})</span>
              <button 
                onClick={() => handleDelete(user.id)} 
                className="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 transition-colors"
              >
                删除
              </button>
            </li>
          ))}
        </ul>
      </main>
    </div>
  )
}