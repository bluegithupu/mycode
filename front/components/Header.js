import Link from 'next/link'

export default function Header() {
  return (
    <header className="bg-blue-600 text-white">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex justify-between items-center">
          <Link href="/">
            <a className="text-2xl font-bold">MyApp</a>
          </Link>
          <ul className="flex space-x-4">
            <li><Link href="/"><a className="hover:text-blue-200 transition-colors">首页</a></Link></li>
            <li><Link href="/about"><a className="hover:text-blue-200 transition-colors">关于</a></Link></li>
          </ul>
        </nav>
      </div>
    </header>
  )
}