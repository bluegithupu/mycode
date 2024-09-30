import { openDb } from '../../../lib/db'

export default async function handler(req, res) {
  const db = openDb()

  switch (req.method) {
    case 'GET':
      try {
        const users = await db.all('SELECT * FROM users')
        res.status(200).json(users)
      } catch (error) {
        res.status(500).json({ error: error.message })
      }
      break

    case 'POST':
      const { name, email } = req.body
      try {
        // 修改这里：使用 get 方法来获取插入的 ID
        await db.run(
          'INSERT INTO users (name, email) VALUES (?, ?)',
          [name, email]
        )
        const result = await db.get('SELECT last_insert_rowid() as id')
        res.status(201).json({ id: result.id, name, email })
      } catch (error) {
        res.status(400).json({ error: error.message })
      }
      break

    default:
      res.status(405).end() // Method Not Allowed
  }
}