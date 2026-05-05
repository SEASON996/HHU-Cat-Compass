// Token 存储 key
const TOKEN_KEY = 'cat_token'
const USER_KEY = 'cat_user'

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY)
}

export const setToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token)
}

export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY)
}

export const getUser = () => {
  const userStr = localStorage.getItem(USER_KEY)
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch {
      return null
    }
  }
  return null
}

export const setUser = (user) => {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export const removeUser = () => {
  localStorage.removeItem(USER_KEY)
}

export const clearAuth = () => {
  removeToken()
  removeUser()
}
