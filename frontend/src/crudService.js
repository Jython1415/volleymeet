import api from './axios';

// fetches all the events
export const fetchEvents = () => api.get('/events')

// adds a new event
export const addEvent = (event) => api.post('/events', event)

// updates an event
export const updateEvent = (eventId, updatedEvent) => api.put(`/events/${eventId}`, updatedEvent)

// delets an event
export const deleteEvent = (eventId) => api.delete(`/events/${eventId}`)
