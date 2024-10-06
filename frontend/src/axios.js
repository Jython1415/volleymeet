import axios from 'axios'

const api = axios.create({
  baseURL: 'http://your-persistence-layer-url/api', // TODO: replace with acutal api
})

export default api
