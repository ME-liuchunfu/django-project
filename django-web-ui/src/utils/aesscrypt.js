// 引入CryptoJS
import CryptoJS from 'crypto-js';

export function encryptData(data, secretKey, iv) {
      const key = CryptoJS.enc.Utf8.parse(secretKey);
      if (!iv) {
          iv = secretKey.substring(0, 16);
      }
      const ivHex = CryptoJS.enc.Utf8.parse(iv); // 使用密钥的前16个字符作为IV

      const encrypted = CryptoJS.AES.encrypt(data, key, {
        iv: ivHex,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
      });

      return encrypted.toString();
    };

export function decryptData(encryptedData, secretKey) {
      const key = CryptoJS.enc.Utf8.parse(secretKey);
      const iv = CryptoJS.enc.Utf8.parse(secretKey.substring(0, 16)); // 使用密钥的前16个字符作为IV

      const decrypted = CryptoJS.AES.decrypt(encryptedData, key, {
        keySize: 128 / 8,
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
      });

      return CryptoJS.enc.Utf8.stringify(decrypted);
    }


