import { Link } from 'react-router-dom'
import { Search, Bot, ArrowRight } from 'lucide-react'

function Home() {
  return (
    <div className="animate-[fadeIn_400ms_var(--ease-out)_both] p-6 max-w-[1200px] mx-auto w-full overflow-y-auto h-full">
      {/* Hero */}
      <div className="text-center pb-4">
        <h1 className="text-[28px] font-bold text-text-primary mb-2">智能徒步助手</h1>
        <p className="text-sm text-text-secondary">知识检索 × 行动执行，让徒步准备更简单</p>
      </div>

      <div className="border-t border-border mb-4" />

      {/* Module Cards */}
      <div className="grid grid-cols-2 gap-5 mb-8 max-md:grid-cols-1">
        <div
          className="bg-white rounded-md p-6 border border-border transition-all duration-300 ease-[var(--ease-out)] hover:shadow-md hover:-translate-y-0.5 hover:border-primary/20 group"
          style={{ animation: 'fadeUp 400ms var(--ease-out) 50ms both' }}
        >
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-sm bg-primary/10 text-primary-light flex items-center justify-center text-2xl transition-all duration-300 ease-[var(--ease-out)] group-hover:scale-105 group-hover:bg-primary/15">
              <Search className="w-7 h-7" strokeWidth={1.5} />
            </div>
            <div>
              <div className="text-lg font-semibold">RAG 模块</div>
              <div className="inline-block px-2 py-0.5 bg-primary/10 text-primary-light text-xs rounded mt-1">对话式界面</div>
            </div>
          </div>
          <p className="text-sm text-text-secondary mb-4 leading-relaxed">
            知识聊天助手，专注于徒步知识问答与检索。
          </p>
          <Link
            to="/love-master"
            className="inline-flex items-center gap-1.5 px-5 py-2 bg-primary text-white rounded-sm text-sm transition-all duration-200 ease-[var(--ease-out)] hover:bg-primary-hover active:scale-[0.97]"
          >
            进入对话
            <ArrowRight className="w-4 h-4 transition-transform duration-200 ease-[var(--ease-out)] group-hover:translate-x-0.5" />
          </Link>
        </div>

        <div
          className="bg-white rounded-md p-6 border border-border transition-all duration-300 ease-[var(--ease-out)] hover:shadow-md hover:-translate-y-0.5 hover:border-primary/20 group"
          style={{ animation: 'fadeUp 400ms var(--ease-out) 120ms both' }}
        >
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-sm bg-primary/10 text-primary-light flex items-center justify-center text-2xl transition-all duration-300 ease-[var(--ease-out)] group-hover:scale-105 group-hover:bg-primary/15">
              <Bot className="w-7 h-7" strokeWidth={1.5} />
            </div>
            <div>
              <div className="text-lg font-semibold">Agent 模块</div>
              <div className="inline-block px-2 py-0.5 bg-primary/10 text-primary-light text-xs rounded mt-1">对话式界面</div>
            </div>
          </div>
          <p className="text-sm text-text-secondary mb-4 leading-relaxed">
            行动/规划聊天助手，专注于行程规划与执行。
          </p>
          <Link
            to="/super-agent"
            className="inline-flex items-center gap-1.5 px-5 py-2 bg-primary text-white rounded-sm text-sm transition-all duration-200 ease-[var(--ease-out)] hover:bg-primary-hover active:scale-[0.97]"
          >
            进入对话
            <ArrowRight className="w-4 h-4 transition-transform duration-200 ease-[var(--ease-out)] group-hover:translate-x-0.5" />
          </Link>
        </div>
      </div>

    </div>
  )
}

export default Home
