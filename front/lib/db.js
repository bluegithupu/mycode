import sqlite3 from 'sqlite3'
import { promisify } from 'util'

let db

// 初始化数据库
function openDb() {
  if (!db) {
    db = new sqlite3.Database('./mydb.sqlite', (err) => {
      if (err) {
        console.error(err.message)
      }
      console.log('Connected to the SQLite database.')
    })
    db.run = promisify(db.run)
    db.get = promisify(db.get)
    db.all = promisify(db.all)
    createTable()
  }
  return db
}

// 创建用户表
async function createTable() {
  const sql = `
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT UNIQUE
    )
  `
  try {
    await db.run(sql)
    console.log('Users table created or already exists.')
  } catch (err) {
    console.error('Error creating users table:', err.message)
  }
}

export { openDb }