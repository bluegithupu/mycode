import { openDb } from '../../../lib/db'

export default async function handler(req, res) {
  const db = openDb()
  const { id } = req.query

  switch (req.method) {
    case 'GET':
      try {
        const user = await db.get('SELECT * FROM users WHERE id = ?', [id])
        if (user) {
          res.status(200).json(user)
        } else {
          res.status(404).json({ message: '用户未找到' })
        }
      } catch (error) {
        res.status(500).json({ error: error.message })
      }
      break

    case 'PUT':
      const { name, email } = req.body
      try {
        await db.run(
          'UPDATE users SET name = ?, email = ? WHERE id = ?',
          [name, email, id]
        )
        res.status(200).json({ id, name, email })
      } catch (error) {
        res.status(400).json({ error: error.message })
      }
      break

    case 'DELETE':
      try {
        await db.run('DELETE FROM users WHERE id = ?', [id])
        res.status(200).json({ message: '用户已删除' })
      } catch (error) {
        res.status(500).json({ error: error.message })
      }
      break

    default:
      res.status(405).end() // Method Not Allowed
  }
}