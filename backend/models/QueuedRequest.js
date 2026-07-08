const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const db = new sqlite3.Database(path.join(__dirname, '../queue_management.db'));

// Initialize database
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS queued_requests (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      title TEXT NOT NULL,
      description TEXT,
      status TEXT DEFAULT 'pending',
      assigned_to INTEGER,
      points_offered INTEGER DEFAULT 0,
      points_given INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      completed_at DATETIME,
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (assigned_to) REFERENCES users(id)
    )
  `);
});

class QueuedRequest {
  static async create(userId, title, description, pointsOffered) {
    return new Promise((resolve, reject) => {
      db.run(
        `INSERT INTO queued_requests (user_id, title, description, points_offered) VALUES (?, ?, ?, ?)`,
        [userId, title, description, pointsOffered],
        function (err) {
          if (err) reject(err);
          else resolve({ id: this.lastID });
        }
      );
    });
  }

  static async findById(id) {
    return new Promise((resolve, reject) => {
      db.get(`SELECT * FROM queued_requests WHERE id = ?`, [id], (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }

  static async getAll(status = null) {
    return new Promise((resolve, reject) => {
      let query = `SELECT * FROM queued_requests`;
      let params = [];
      if (status) {
        query += ` WHERE status = ?`;
        params = [status];
      }
      query += ` ORDER BY created_at DESC`;
      db.all(query, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  }

  static async getByUserId(userId) {
    return new Promise((resolve, reject) => {
      db.all(
        `SELECT * FROM queued_requests WHERE user_id = ? ORDER BY created_at DESC`,
        [userId],
        (err, rows) => {
          if (err) reject(err);
          else resolve(rows);
        }
      );
    });
  }

  static async getAssignedToUser(userId) {
    return new Promise((resolve, reject) => {
      db.all(
        `SELECT * FROM queued_requests WHERE assigned_to = ? ORDER BY created_at DESC`,
        [userId],
        (err, rows) => {
          if (err) reject(err);
          else resolve(rows);
        }
      );
    });
  }

  static async assign(requestId, userId) {
    return new Promise((resolve, reject) => {
      db.run(
        `UPDATE queued_requests SET assigned_to = ?, status = 'assigned' WHERE id = ?`,
        [userId, requestId],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }

  static async complete(requestId, pointsGiven) {
    return new Promise((resolve, reject) => {
      db.run(
        `UPDATE queued_requests SET status = 'completed', points_given = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?`,
        [pointsGiven, requestId],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }

  static async updateStatus(requestId, status) {
    return new Promise((resolve, reject) => {
      db.run(
        `UPDATE queued_requests SET status = ? WHERE id = ?`,
        [status, requestId],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }
}

module.exports = QueuedRequest;
