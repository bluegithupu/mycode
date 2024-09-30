export default function handler(req, res) {
  // 生成一个1到100之间的随机数
  const randomNumber = Math.floor(Math.random() * 100) + 1

  // 返回随机数据
  res.status(200).json({ 
    number: randomNumber,
    message: `这是一个1到100之间的随机数: ${randomNumber}`
  })
}