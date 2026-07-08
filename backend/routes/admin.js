const express = require('express');
const User = require('../models/User');
const QueuedRequest = require('../models/QueuedRequest');
const { verifyToken, verifyAdmin } = require('../middleware/auth');

const router = express.Router();

// Get all users
router.get('/users', verifyToken, verifyAdmin, async (req, res) => {
  try {
    const users = await User.getAll();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all queued requests
router.get('/requests', verifyToken, verifyAdmin, async (req, res) => {
  try {
    const requests = await QueuedRequest.getAll();
    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Approve request
router.post('/requests/:requestId/approve', verifyToken, verifyAdmin, async (req, res) => {
  try {
    await QueuedRequest.updateStatus(req.params.requestId, 'approved');
    res.json({ message: 'Request approved' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Reject request
router.post('/requests/:requestId/reject', verifyToken, verifyAdmin, async (req, res) => {
  try {
    await QueuedRequest.updateStatus(req.params.requestId, 'rejected');
    res.json({ message: 'Request rejected' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
