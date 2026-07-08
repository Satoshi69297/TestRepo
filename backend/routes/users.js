const express = require('express');
const User = require('../models/User');
const QueuedRequest = require('../models/QueuedRequest');
const { verifyToken } = require('../middleware/auth');

const router = express.Router();

// Get user profile
router.get('/profile/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json({ id: user.id, username: user.username, email: user.email, profile: user.profile, points: user.points });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update user profile
router.put('/profile/:id', verifyToken, async (req, res) => {
  try {
    const { username, email, profile } = req.body;
    if (req.user.id !== parseInt(req.params.id)) {
      return res.status(403).json({ error: 'Unauthorized' });
    }

    await User.update(req.params.id, username, email, profile);
    res.json({ message: 'Profile updated successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Register queued request
router.post('/requests', verifyToken, async (req, res) => {
  try {
    const { title, description, pointsOffered } = req.body;
    const result = await QueuedRequest.create(req.user.id, title, description, pointsOffered || 0);
    res.status(201).json({ id: result.id, message: 'Request created successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user's requests
router.get('/requests', verifyToken, async (req, res) => {
  try {
    const requests = await QueuedRequest.getByUserId(req.user.id);
    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get assigned requests
router.get('/assigned-requests', verifyToken, async (req, res) => {
  try {
    const requests = await QueuedRequest.getAssignedToUser(req.user.id);
    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Acquire (claim) request
router.post('/requests/:requestId/acquire', verifyToken, async (req, res) => {
  try {
    await QueuedRequest.assign(req.params.requestId, req.user.id);
    res.json({ message: 'Request acquired successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Complete request
router.post('/requests/:requestId/complete', verifyToken, async (req, res) => {
  try {
    const { pointsGiven } = req.body;
    const request = await QueuedRequest.findById(req.params.requestId);
    
    if (!request) {
      return res.status(404).json({ error: 'Request not found' });
    }

    if (request.assigned_to !== req.user.id) {
      return res.status(403).json({ error: 'Unauthorized' });
    }

    await QueuedRequest.complete(req.params.requestId, pointsGiven);
    await User.addPoints(req.user.id, pointsGiven);
    
    res.json({ message: 'Request completed successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
