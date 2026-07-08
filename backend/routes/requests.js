const express = require('express');
const QueuedRequest = require('../models/QueuedRequest');

const router = express.Router();

// Get all pending requests
router.get('/', async (req, res) => {
  try {
    const requests = await QueuedRequest.getAll('pending');
    res.json(requests);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get request by ID
router.get('/:id', async (req, res) => {
  try {
    const request = await QueuedRequest.findById(req.params.id);
    if (!request) {
      return res.status(404).json({ error: 'Request not found' });
    }
    res.json(request);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
