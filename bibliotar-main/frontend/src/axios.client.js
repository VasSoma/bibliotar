import axios from 'axios'

async function getData() {
  try {
    const result = await axios.get('serverhost.com/api/books')
    result.data
  } catch (error) {
    console.error(error)
  }
}
