import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import {
  Mountain,
  Home,
  Search,
  Bot,
} from 'lucide-react'
import HomePage from './pages/Home'
import LoveMaster from './pages/LoveMaster'
import SuperAgent from './pages/SuperAgent'
import LlmConfig from './pages/LlmConfig'

function App() {
  const location = useLocation()

  const getHeaderTitle = () => {
    if (location.pathname === '/love-master') return 'RAG 模块'
    if (location.pathname === '/super-agent') return 'Agent 模块'
    if (location.pathname === '/llm-config') return 'LLM 配置'
    return '智能徒步助手'
  }

  return (
    <div className="flex min-h-[100dvh] overflow-hidden">
      {/* Sidebar */}
      <aside className="fixed top-0 left-0 bottom-0 z-[100] w-sidebar flex flex-col overflow-hidden bg-primary text-white max-md:hidden">
        <div className="flex items-center gap-2.5 px-5 py-4 border-b border-white/10">
          <div className="flex items-center justify-center w-8 h-8 shrink-0">
            <Mountain className="w-7 h-7" strokeWidth={2} />
          </div>
          <span className="text-[15px] font-semibold text-white">智能徒步助手</span>
        </div>
        <nav className="flex-1 py-3">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center gap-3 px-5 py-3 mx-3 rounded-sm text-sm transition-all ${
                isActive ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/[0.08] hover:text-white'
              }`
            }
            end
          >
            <Home className="w-[18px] h-[18px]" strokeWidth={2} />
            <span>首页</span>
          </NavLink>
          <NavLink
            to="/love-master"
            className={({ isActive }) =>
              `flex items-center gap-3 px-5 py-3 mx-3 rounded-sm text-sm transition-all ${
                isActive ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/[0.08] hover:text-white'
              }`
            }
          >
            <Search className="w-[18px] h-[18px]" strokeWidth={2} />
            <span>RAG 模块</span>
          </NavLink>
          <NavLink
            to="/super-agent"
            className={({ isActive }) =>
              `flex items-center gap-3 px-5 py-3 mx-3 rounded-sm text-sm transition-all ${
                isActive ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/[0.08] hover:text-white'
              }`
            }
          >
            <Bot className="w-[18px] h-[18px]" strokeWidth={2} />
            <span>Agent 模块</span>
          </NavLink>
        </nav>
        {/* Forest Decoration */}
        <div className="absolute bottom-0 left-0 right-0 h-[180px] pointer-events-none opacity-[0.15]">
          <svg viewBox="0 0 220 180" fill="currentColor" preserveAspectRatio="xMidYMax slice">
            <path d="M0 180 L0 140 Q20 120 40 130 Q60 100 80 120 Q100 90 120 110 Q140 80 160 100 Q180 70 200 90 Q210 85 220 95 L220 180 Z" opacity="0.6" />
            <path d="M0 180 L0 150 Q30 130 50 145 Q70 115 90 135 Q110 105 130 125 Q150 95 170 115 Q190 90 220 110 L220 180 Z" opacity="0.4" />
          </svg>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 min-w-0 flex flex-col ml-sidebar max-md:ml-0">
        <header className="sticky top-0 z-50 h-header flex items-center justify-between px-6 bg-white border-b border-border">
          <div className="text-base font-semibold text-text-primary">{getHeaderTitle()}</div>
          {/* Header actions removed per request */}
        </header>

        <main className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/love-master" element={<LoveMaster />} />
            <Route path="/super-agent" element={<SuperAgent />} />
            <Route path="/llm-config" element={<LlmConfig />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App
