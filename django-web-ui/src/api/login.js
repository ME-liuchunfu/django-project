import request from '@/utils/request'
import {encryptData} from '@/utils/aesscrypt'
const df_secretKey = "694390bf-c759-4f5a-8444-723b46d4"

// 登录方法
export function login(username, password, code, uuid, encryptFlag, secretKey) {
  const data = {
    username,
    password,
    code,
    uuid
  }
  let form_data = data
  if (encryptFlag) {
      if (!secretKey) {
        secretKey = df_secretKey
      }
      const encry_data = encryptData(JSON.stringify(data), secretKey)
      form_data = {
          "params": encry_data,
          "encrypt": true
      }
  }
  return request({
    url: '/login',
    headers: {
      isToken: false,
      repeatSubmit: false
    },
    method: 'post',
    data: form_data
  })
}

// 注册方法
export function register(data) {
  return request({
    url: '/register',
    headers: {
      isToken: false
    },
    method: 'post',
    data: data
  })
}

// 获取用户详细信息
export function getInfo() {
  return request({
    url: '/getInfo',
    method: 'get'
  })
}

// 退出方法
export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}

// 获取验证码
export function getCodeImg() {
  return request({
    url: '/captchaImage',
    headers: {
      isToken: false
    },
    method: 'get',
    timeout: 20000
  })
}
