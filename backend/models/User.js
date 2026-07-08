const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const db = new sqlite3.Database(path.join(__dirname, '../queue_management.db'));

// Initialize database
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      profile TEXT,
      points INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
});

class User {
  static async create(username, email, password, profile) {
    return new Promise((resolve, reject) => {
      db.run(
        `INSERT INTO users (username, email, password, profile) VALUES (?, ?, ?, ?)`,
        [username, email, password, profile],
        function (err) {
          if (err) reject(err);
          else resolve({ id: this.lastID });
        }
      );
    });
  }

  static async findById(id) {
    return new Promise((resolve, reject) => {
      db.get(`SELECT * FROM users WHERE id = ?`, [id], (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }

  static async findByUsername(username) {
    return new Promise((resolve, reject) => {
      db.get(`SELECT * FROM users WHERE username = ?`, [username], (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }

  static async findByEmail(email) {
    return new Promise((resolve, reject) => {
      db.get(`SELECT * FROM users WHERE email = ?`, [email], (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }

  static async update(id, username, email, profile) {
    return new Promise((resolve, reject) => {
      db.run(
        `UPDATE users SET username = ?, email = ?, profile = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?`,
        [username, email, profile, id],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }

  static async getAll() {
    return new Promise((resolve, reject) => {
      db.all(`SELECT id, username, email, profile, points, created_at FROM users`, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  }

  static async addPoints(userId, points) {
    return new Promise((resolve, reject) => {
      db.run(
        `UPDATE users SET points = points + ? WHERE id = ?`,
        [points, userId],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }
}

module.exports = User;
