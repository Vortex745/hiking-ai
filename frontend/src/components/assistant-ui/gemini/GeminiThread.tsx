import {
  AuiIf,
  ComposerPrimitive,
  ThreadPrimitive,
  MessagePrimitive,
  useMessage,
} from "@assistant-ui/react";
import { ArrowUp, RotateCw, Copy, Check, MoreHorizontal, Pin, PinOff, GripHorizontal } from 'lucide-react';
import { getConversationMemoryProgress } from '../../../api/conversationMemory';
import { useRef, useState, createContext, useContext, useCallback, useEffect, type RefObject, type PointerEvent as ReactPointerEvent } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(useGSAP);

interface GeminiThreadProps {
  emptyTitle: string;
  /** Called when user clicks "regenerate" — parent should resend the last user prompt */
  onRegenerate?: () => void;
  /** Real message count from the parent page's state (for accurate memory meter) */
  realMessageCount?: number;
}

/** Context to pass callbacks down to ChatMessage without prop drilling */
const ThreadActionsContext = createContext<{
  onRegenerate?: () => void;
  realMessageCount: number;
}>({ realMessageCount: 0 });

export const GeminiThread = ({ emptyTitle, onRegenerate, realMessageCount = 0 }: GeminiThreadProps) => (
  <ThreadActionsContext.Provider value={{ onRegenerate, realMessageCount }}>
    <ThreadPrimitive.Root className="h-full bg-[#fdfcfc] dark:bg-[#131314] flex flex-col overflow-hidden w-full relative">
      <AuiIf condition={(s) => s.thread.isEmpty}>
        <EmptyState emptyTitle={emptyTitle} />
      </AuiIf>
      <AuiIf condition={(s) => !s.thread.isEmpty}>
        <div className="flex-1 overflow-hidden flex flex-col relative w-full">
          <ThreadPrimitive.Viewport className="flex-1 overflow-y-auto px-4 md:px-8 pt-8 pb-32 scrollbar-thin">
            <ThreadPrimitive.Messages components={{ Message: ChatMessage }} />
          </ThreadPrimitive.Viewport>
          <div className="absolute bottom-0 left-0 right-0 pt-10 pb-4 bg-gradient-to-t from-[#fdfcfc] via-[#fdfcfc] dark:from-[#131314] dark:via-[#131314] to-transparent pointer-events-none">
            <div className="pointer-events-auto">
              <Composer />
            </div>
          </div>
        </div>
      </AuiIf>
    </ThreadPrimitive.Root>
  </ThreadActionsContext.Provider>
);

const EmptyState = ({ emptyTitle }: { emptyTitle: string }) => (
  <div className="relative flex grow h-full items-center justify-center">
    <div
      aria-hidden="true"
      className="pointer-events-none absolute top-1/2 left-1/2 h-[330px] w-[720px] -translate-x-1/2 -translate-y-1/2 bg-[radial-gradient(closest-side,#a9d1fb,transparent)] opacity-70 blur-[55px] dark:bg-[radial-gradient(closest-side,#1d4068,transparent)] dark:opacity-65"
    />
    <div className="relative z-10 w-full max-w-[800px] px-6 flex flex-col items-center">
      <h1 className="text-center text-3xl font-medium mb-12 text-[#1f1f1f] dark:text-[#e3e3e3]">{emptyTitle}</h1>
      <Composer />
    </div>
  </div>
);

const Composer = () => (
  <ComposerPrimitive.Root className="flex flex-col rounded-3xl bg-white p-2.5 shadow-[0_2px_10px_-2px_rgba(0,0,0,0.18)] dark:bg-[#1e1f20] w-full max-w-[800px] mx-auto border border-black/5 dark:border-white/5">
    <div className="flex items-end gap-2 px-2">
      <ComposerPrimitive.Input
        placeholder="输入您的问题..."
        className="flex-1 resize-none bg-transparent text-[16px] outline-none border-none py-1.5 min-h-[32px] text-[#1f1f1f] dark:text-[#e3e3e3] placeholder:text-[#444746] dark:placeholder:text-[#c4c7c5]"
      />
      
      {/* Send: disabled grey when empty, blue when there is text */}
      <AuiIf condition={(s) => !s.thread.isRunning}>
        <ComposerPrimitive.Send className="bg-[#d3e3fd] text-[#062e6f] disabled:bg-[#e8eaed] disabled:text-[#1f1f1f]/40 dark:disabled:bg-[#333537] dark:disabled:text-[#c4c7c5]/40 p-2 rounded-full transition-colors flex shrink-0 h-10 w-10 items-center justify-center press-scale">
          <ArrowUp className="w-[18px] h-[18px]" strokeWidth={2.5} />
        </ComposerPrimitive.Send>
      </AuiIf>
      
      {/* Cancel: stop square while a response streams */}
      <AuiIf condition={(s) => s.thread.isRunning}>
        <ComposerPrimitive.Cancel className="bg-[#d3e3fd] text-[#062e6f] p-2 rounded-full transition-colors flex shrink-0 h-10 w-10 items-center justify-center press-scale">
          <span className="size-3 rounded-[3px] bg-current" />
        </ComposerPrimitive.Cancel>
      </AuiIf>
    </div>
  </ComposerPrimitive.Root>
);

const sourceLabel = (source: string) => {
  if (source === 'feishu') return '飞书'
  if (source === 'upload') return '上传文档'
  if (source === 'unknown') return '未知来源'
  return source
}

const MarkdownText = (part: any) => {
  return (
    <div className="whitespace-pre-wrap leading-relaxed relative">
      {part.text || part.part?.text}
    </div>
  );
};

const CustomToolCall = (part: any) => {
  const toolName = part.toolName || part.part?.toolName;
  const args = part.args || part.part?.args;
  
  if (toolName === "processSteps") {
    return null;
  }
  
  if (toolName === "traceEvents") {
    return null;
  }

  if (toolName === "artifacts") {
    const artifacts = args as any[];
    if (!artifacts || artifacts.length === 0) return null;
    return (
      <div className="mt-3 border-t border-border/40 pt-3">
        {artifacts.map((artifact, i) => (
          <div key={i} className="flex items-start gap-2 text-[13px] text-text-secondary mb-2 last:mb-0">
             <span className="shrink-0 mt-0.5 opacity-70">📋</span>
             <span className="leading-relaxed">{artifact.content}</span>
          </div>
        ))}
      </div>
    );
  }

  if (part.toolName === "searchSummary") {
    const summary = part.args;
    if (!summary || summary.documents.length === 0) return null;
    return (
      <details className="mt-4 border-t border-border/40 pt-3 text-[13px] text-text-secondary">
        <summary className="cursor-pointer select-none font-medium text-text-primary outline-none">
          文档搜索 · {summary.searchedCount} 篇文档 / {summary.matchedChunks} 个片段
        </summary>
        <div className="mt-3 space-y-3 opacity-90">
          {summary.documents.map((doc: any, idx: number) => (
            <div key={`${doc.title}-${idx}`} className="border-l-2 border-primary/25 pl-3">
              <div className="font-medium text-text-primary">
                {idx + 1}. {doc.title}
              </div>
              <div className="text-[12px] mt-0.5 opacity-70">
                来源：{sourceLabel(doc.source)}
                {doc.chunks ? ` · ${doc.chunks} 个片段` : ''}
              </div>
              {doc.content && (
                <div className="mt-1.5 whitespace-pre-wrap text-text-secondary">
                  {doc.content}
                </div>
              )}
            </div>
          ))}
        </div>
      </details>
    );
  }

  return null;
};

type LifecycleStep = {
  title: string;
  detail: string;
  state: 'complete' | 'active' | 'pending';
};

type LifecyclePosition = {
  x: number;
  y: number;
};

const LIFECYCLE_PANEL_WIDTH = 330;
const LIFECYCLE_PANEL_HEIGHT = 420;
const LIFECYCLE_PANEL_MARGIN = 12;

function prefersReducedMotion() {
  return typeof window !== 'undefined'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

const traceLabels: Record<string, string> = {
  thought: '思考',
  process: '流程',
  documents: '文档',
  tool_call: '工具调用',
  tool_result: '工具结果',
  approval_required: '需要确认',
  artifact: '产物',
  text: '回答',
  done: '完成',
  error: '错误',
};

function getPartToolName(part: any) {
  return part?.toolName || part?.part?.toolName || part?.tool_name || '';
}

function getPartArgs(part: any) {
  return part?.args ?? part?.part?.args ?? part?.result ?? null;
}

function getToolArgs(content: readonly any[], toolName: string) {
  const part = content.find(item => getPartToolName(item) === toolName);
  return part ? getPartArgs(part) : null;
}

function getMessageText(content: readonly any[]) {
  return content
    .filter(part => part?.type === 'text' || typeof part?.text === 'string')
    .map(part => part.text || part.part?.text || '')
    .join('');
}

function stepState(done: boolean, active: boolean): LifecycleStep['state'] {
  if (done) return 'complete';
  if (active) return 'active';
  return 'pending';
}

function getAgentLifecycle(events: any[], isRunning: boolean, hasText: boolean): LifecycleStep[] {
  const phases = new Set(events.map(event => event?.metadata?.phase).filter(Boolean));
  const hasToolEvent = events.some(event => ['tool_call', 'tool_result', 'approval_required'].includes(event?.type));

  return [
    {
      title: '请求理解',
      detail: '识别徒步意图、场景和缺失信息',
      state: stepState(events.length > 0, isRunning && events.length === 0),
    },
    {
      title: '记忆读取',
      detail: '读取会话历史、摘要和长期记忆',
      state: stepState(phases.has('memory'), isRunning && events.length > 0 && !phases.has('memory')),
    },
    {
      title: '查询改写',
      detail: '把用户问题整理成更适合工具执行的任务',
      state: stepState(phases.has('query_rewrite'), isRunning && phases.has('memory') && !phases.has('query_rewrite')),
    },
    {
      title: '工具编排',
      detail: '按风险等级选择并执行徒步工具',
      state: stepState(hasToolEvent, isRunning && phases.has('start') && !hasToolEvent && !hasText),
    },
    {
      title: '回答生成',
      detail: '整合工具结果并流式生成回复',
      state: stepState(hasText, isRunning && !hasText),
    },
    {
      title: '完成收尾',
      detail: '结束 SSE、提交可沉淀的会话记忆',
      state: stepState(!isRunning && hasText, false),
    },
  ];
}

function getRagLifecycle(processSteps: string[], hasSearchSummary: boolean, isRunning: boolean, hasText: boolean): LifecycleStep[] {
  const hasProcess = processSteps.length > 0;

  return [
    {
      title: '接收问题',
      detail: '构建 RAG 查询载荷并打开 SSE 连接',
      state: 'complete',
    },
    {
      title: '查询理解',
      detail: '进行简单问题识别或查询改写',
      state: stepState(hasProcess || hasText || hasSearchSummary, isRunning && !hasProcess && !hasText),
    },
    {
      title: '知识检索',
      detail: '向量检索、BM25 召回和候选片段融合',
      state: stepState(hasSearchSummary, isRunning && hasProcess && !hasSearchSummary && !hasText),
    },
    {
      title: '上下文组装',
      detail: '筛选命中文档并准备回答上下文',
      state: stepState(hasSearchSummary || hasText, isRunning && hasSearchSummary && !hasText),
    },
    {
      title: '回答生成',
      detail: '根据上下文流式输出最终回复',
      state: stepState(hasText, isRunning && !hasText),
    },
    {
      title: '完成收尾',
      detail: '发送 done 事件并关闭本次流',
      state: stepState(!isRunning && hasText, false),
    },
  ];
}

function getGenericLifecycle(isRunning: boolean, hasText: boolean): LifecycleStep[] {
  return [
    {
      title: '建立连接',
      detail: '向后端发送请求并等待首个 SSE 事件',
      state: stepState(hasText, isRunning && !hasText),
    },
    {
      title: '回答生成',
      detail: '接收 text 事件并增量更新消息',
      state: stepState(hasText, isRunning && !hasText),
    },
    {
      title: '完成收尾',
      detail: '接收 done 事件后解除运行状态',
      state: stepState(!isRunning && hasText, false),
    },
  ];
}

function buildLifecycle(content: readonly any[], isRunning: boolean) {
  const text = getMessageText(content).trim();
  const hasText = text.length > 0;
  const traceEvents = (getToolArgs(content, 'traceEvents') || []) as any[];
  const processSteps = (getToolArgs(content, 'processSteps') || []) as string[];
  const searchSummary = getToolArgs(content, 'searchSummary') as any;

  if (traceEvents.length > 0) {
    return {
      title: 'Agent 技术生命周期',
      steps: getAgentLifecycle(traceEvents, isRunning, hasText),
      recentEvents: traceEvents.slice(-4).map(event => ({
        label: traceLabels[event?.type] || event?.type || '事件',
        content: String(event?.content || '').trim(),
      })).filter(event => event.content),
    };
  }

  if (processSteps.length > 0 || searchSummary) {
    const documentCount = typeof searchSummary?.searchedCount === 'number'
      ? `命中 ${searchSummary.searchedCount} 篇文档 / ${searchSummary.matchedChunks || 0} 个片段`
      : '';
    return {
      title: 'RAG 技术生命周期',
      steps: getRagLifecycle(processSteps, Boolean(searchSummary), isRunning, hasText),
      recentEvents: [
        ...processSteps.slice(-3).map(step => ({ label: '流程', content: step })),
        ...(documentCount ? [{ label: '检索', content: documentCount }] : []),
      ],
    };
  }

  return {
    title: '流式回复生命周期',
    steps: getGenericLifecycle(isRunning, hasText),
    recentEvents: [],
  };
}

function clampLifecyclePosition(position: LifecyclePosition): LifecyclePosition {
  if (typeof window === 'undefined') return position;

  const maxX = Math.max(
    LIFECYCLE_PANEL_MARGIN,
    window.innerWidth - LIFECYCLE_PANEL_WIDTH - LIFECYCLE_PANEL_MARGIN,
  );
  const maxY = Math.max(
    LIFECYCLE_PANEL_MARGIN,
    window.innerHeight - LIFECYCLE_PANEL_HEIGHT - LIFECYCLE_PANEL_MARGIN,
  );

  return {
    x: Math.min(Math.max(position.x, LIFECYCLE_PANEL_MARGIN), maxX),
    y: Math.min(Math.max(position.y, LIFECYCLE_PANEL_MARGIN), maxY),
  };
}

function AiThinking({ text = '思考中' }: { text?: string }) {
  return (
    <div className="ai-thinking mt-1" role="status" aria-label="AI 正在思考">
      <span className="ai-thinking-core">
        <span />
        <span />
        <span />
      </span>
      <span className="ai-thinking-line" />
      <span className="ai-thinking-label">
        <span key={text} className="ai-thinking-text-scroll">{text}</span>
      </span>
    </div>
  );
}

const LifecycleHoverPanel = ({
  content,
  isRunning,
  pinned,
  position,
  panelRef,
  onPinToggle,
  onDragStart,
}: {
  content: readonly any[];
  isRunning: boolean;
  pinned: boolean;
  position: LifecyclePosition;
  panelRef: RefObject<HTMLDivElement>;
  onPinToggle: () => void;
  onDragStart: (event: ReactPointerEvent<HTMLDivElement>) => void;
}) => {
  const lifecycle = buildLifecycle(content, isRunning);

  return (
    <div
      ref={panelRef}
      className={`z-50 w-[330px] rounded-2xl border border-black/10 bg-white/95 p-4 text-left shadow-[0_16px_50px_rgba(0,0,0,0.18)] backdrop-blur-xl dark:border-white/10 dark:bg-[#1e1f20]/95 ${
        pinned
          ? 'fixed left-0 top-0 max-h-[72vh] overflow-y-auto will-change-transform'
          : 'absolute bottom-full left-1/2 mb-2 -translate-x-1/2'
      }`}
      style={pinned ? { transform: `translate3d(${position.x}px, ${position.y}px, 0)` } : undefined}
      data-lifecycle-panel={pinned ? 'pinned' : 'hover'}
    >
      <div
        className={`mb-3 flex items-center justify-between gap-3 ${pinned ? 'cursor-grab active:cursor-grabbing' : ''}`}
        onPointerDown={onDragStart}
      >
        <div className="min-w-0 text-[13px] font-medium text-[#1f1f1f] dark:text-[#e3e3e3]">
          {lifecycle.title}
        </div>
        <div className="flex shrink-0 items-center gap-1">
          {pinned && <GripHorizontal className="h-3.5 w-3.5 text-[#5f6368] dark:text-[#bdc1c6]" strokeWidth={1.7} />}
          <button
            type="button"
            className="rounded-full p-1 text-[#5f6368] transition-colors hover:bg-black/5 hover:text-[#1f1f1f] dark:text-[#bdc1c6] dark:hover:bg-white/10 dark:hover:text-[#e3e3e3]"
            aria-pressed={pinned}
            aria-label={pinned ? '取消钉住流程' : '钉住流程'}
            title={pinned ? '取消钉住' : '钉住流程'}
            onPointerDown={(event) => {
              event.preventDefault();
              event.stopPropagation();
            }}
            onClick={onPinToggle}
          >
            {pinned
              ? <PinOff className="h-3.5 w-3.5" strokeWidth={1.8} />
              : <Pin className="h-3.5 w-3.5" strokeWidth={1.8} />
            }
          </button>
        </div>
      </div>
      <div className="space-y-2.5">
        {lifecycle.steps.map((step, index) => (
          <div key={`${step.title}-${index}`} className="grid grid-cols-[18px_1fr] gap-2">
            <span
              className={`mt-1 h-2.5 w-2.5 rounded-full ${
                step.state === 'complete'
                  ? 'bg-[#0b57d0]'
                  : step.state === 'active'
                    ? 'bg-[#0b57d0] shadow-[0_0_0_5px_rgba(11,87,208,0.12)] animate-pulse'
                    : 'bg-black/15 dark:bg-white/20'
              }`}
            />
            <span>
              <span className="block text-[12px] font-medium text-[#1f1f1f] dark:text-[#e3e3e3]">
                {step.title}
              </span>
              <span className="block text-[11px] leading-snug text-[#5f6368] dark:text-[#bdc1c6]">
                {step.detail}
              </span>
            </span>
          </div>
        ))}
      </div>
      {lifecycle.recentEvents.length > 0 && (
        <div className="mt-3 border-t border-black/10 pt-3 dark:border-white/10">
          <div className="mb-2 text-[11px] font-medium text-[#5f6368] dark:text-[#bdc1c6]">最近事件</div>
          <div className="space-y-1.5">
            {lifecycle.recentEvents.map((event, index) => (
              <div key={`${event.label}-${index}`} className="text-[11px] leading-snug text-[#444746] dark:text-[#c4c7c5]">
                <span className="font-medium text-[#1f1f1f] dark:text-[#e3e3e3]">{event.label}：</span>
                {event.content}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const ChatMessage = () => {
  const msgRef = useRef<HTMLDivElement>(null);
  const lifecycleAnchorRef = useRef<HTMLDivElement>(null);
  const { onRegenerate, realMessageCount } = useContext(ThreadActionsContext);
  const [copied, setCopied] = useState(false);
  const [showLifecycle, setShowLifecycle] = useState(false);
  const [lifecyclePinned, setLifecyclePinned] = useState(false);
  const [lifecyclePosition, setLifecyclePosition] = useState<LifecyclePosition>(() => ({
    x: LIFECYCLE_PANEL_MARGIN,
    y: 96,
  }));
  const lifecyclePanelRef = useRef<HTMLDivElement>(null);
  const lifecyclePositionRef = useRef(lifecyclePosition);
  const messageContent = useMessage((state) => state.content) as any[] || [];
  const messageRole = useMessage((state) => state.role);
  const messageStatusType = useMessage((state) => state.status?.type);
  const isMessageRunning = messageStatusType === 'running';
  const isAssistantThinking = messageRole === 'assistant'
    && isMessageRunning
    && getMessageText(messageContent).trim().length === 0;

  let thinkingText = '思考中';
  if (isAssistantThinking) {
    const lifecycle = buildLifecycle(messageContent, isMessageRunning);
    const activeStep = lifecycle.steps.find(s => s.state === 'active');
    if (activeStep) {
      thinkingText = activeStep.title;
    }
  }

  useEffect(() => {
    lifecyclePositionRef.current = lifecyclePosition;
  }, [lifecyclePosition]);
  
  useGSAP(() => {
    const message = msgRef.current;
    if (!message || prefersReducedMotion()) return;

    gsap.fromTo(message, {
      autoAlpha: 0,
      scale: 0.98,
      y: 8,
      willChange: 'transform, opacity',
    }, {
      autoAlpha: 1,
      scale: 1,
      y: 0,
      duration: 0.22,
      ease: 'power3.out',
      force3D: true,
      overwrite: 'auto',
      clearProps: 'transform,opacity,visibility,willChange',
    });
  }, []);

  const handleCopy = useCallback(() => {
    // Grab the text content from the message DOM node
    const textEl = msgRef.current?.querySelector('.whitespace-pre-wrap');
    const text = textEl?.textContent || '';
    if (!text.trim()) return;
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  }, []);

  const handleRegenerate = useCallback(() => {
    onRegenerate?.();
  }, [onRegenerate]);

  const placePinnedLifecycle = useCallback(() => {
    const rect = lifecycleAnchorRef.current?.getBoundingClientRect();
    const fallback = {
      x: typeof window === 'undefined'
        ? LIFECYCLE_PANEL_MARGIN
        : window.innerWidth - LIFECYCLE_PANEL_WIDTH - 24,
      y: 96,
    };
    if (!rect) {
      setLifecyclePosition(clampLifecyclePosition(fallback));
      return;
    }

    setLifecyclePosition(clampLifecyclePosition({
      x: rect.left + rect.width / 2 - LIFECYCLE_PANEL_WIDTH / 2,
      y: rect.top - LIFECYCLE_PANEL_HEIGHT - 10,
    }));
  }, []);

  const handleLifecyclePinToggle = useCallback(() => {
    if (lifecyclePinned) {
      setLifecyclePinned(false);
      setShowLifecycle(false);
      return;
    }

    placePinnedLifecycle();
    setLifecyclePinned(true);
    setShowLifecycle(true);
  }, [lifecyclePinned, placePinnedLifecycle]);

  const handleLifecycleDragStart = useCallback((event: ReactPointerEvent<HTMLDivElement>) => {
    if (!lifecyclePinned || event.button !== 0) return;

    event.preventDefault();
    try {
      event.currentTarget.setPointerCapture(event.pointerId);
    } catch {
      // Some synthetic/browser combinations do not allow capture here.
    }
    const startX = event.clientX;
    const startY = event.clientY;
    const startPosition = lifecyclePositionRef.current;
    let nextPosition = startPosition;
    let frame = 0;

    const applyDragPosition = () => {
      frame = 0;
      const panel = lifecyclePanelRef.current;
      if (panel) {
        gsap.set(panel, {
          x: nextPosition.x,
          y: nextPosition.y,
          force3D: true,
        });
      }
    };

    const handlePointerMove = (moveEvent: PointerEvent) => {
      const dx = moveEvent.clientX - startX;
      const dy = moveEvent.clientY - startY;
      nextPosition = clampLifecyclePosition({
        x: startPosition.x + dx,
        y: startPosition.y + dy,
      });
      lifecyclePositionRef.current = nextPosition;
      if (!frame) frame = window.requestAnimationFrame(applyDragPosition);
    };

    const handlePointerUp = () => {
      if (frame) window.cancelAnimationFrame(frame);
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointercancel', handlePointerUp);
      setLifecyclePosition(lifecyclePositionRef.current);
    };

    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerup', handlePointerUp, { once: true });
    window.addEventListener('pointercancel', handlePointerUp, { once: true });
  }, [lifecyclePinned]);

  return (
    <MessagePrimitive.Root className="w-full flex flex-col mb-8 max-w-[800px] mx-auto px-4">
      <div ref={msgRef} className="w-full flex flex-col">
        {/* User Message */}
        <AuiIf condition={(s) => s.message.role === "user"}>
          <div className="flex justify-end w-full">
            <div className="max-w-[85%] md:max-w-[75%] rounded-3xl bg-[#f2f0f0] dark:bg-[#333537] px-5 py-2.5 text-[15px] text-[#1f1f1f] dark:text-[#e3e3e3] w-fit break-words">
              <MessagePrimitive.Parts components={{ Text: MarkdownText, ToolCall: CustomToolCall } as any} />
            </div>
          </div>
        </AuiIf>
        
        {/* Assistant Message */}
        <AuiIf condition={(s) => s.message.role === "assistant"}>
          <div className="flex flex-col items-start w-full group">
            <div className="max-w-full text-[15px] text-[#1f1f1f] dark:text-[#e3e3e3] leading-relaxed break-words">
              <MessagePrimitive.Parts components={{ Text: MarkdownText, ToolCall: CustomToolCall } as any} />
              {isAssistantThinking && <AiThinking text={thinkingText} />}
            </div>
            
            {/* Action Bar — only show when not streaming */}
            <AuiIf condition={(s) => !s.message.isLast || !s.thread.isRunning}>
              <div className="flex items-center gap-2 mt-2 text-[#444746] dark:text-[#c4c7c5]">
                <button
                  className="p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors press-scale"
                  onClick={handleRegenerate}
                  title="重新生成"
                >
                  <RotateCw className="w-[15px] h-[15px]" strokeWidth={1.5} />
                </button>
                <button
                  className="p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors press-scale"
                  onClick={handleCopy}
                  title={copied ? "已复制" : "复制"}
                >
                  {copied
                    ? <Check className="w-[15px] h-[15px] text-green-500" strokeWidth={1.5} />
                    : <Copy className="w-[15px] h-[15px]" strokeWidth={1.5} />
                  }
                </button>
                <div
                  ref={lifecycleAnchorRef}
                  className="relative"
                  onMouseEnter={() => setShowLifecycle(true)}
                  onMouseLeave={() => { if (!lifecyclePinned) setShowLifecycle(false); }}
                  onFocus={() => setShowLifecycle(true)}
                  onBlur={() => { if (!lifecyclePinned) setShowLifecycle(false); }}
                >
                  <button
                    className="p-1.5 hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors press-scale"
                    title="思考流程"
                    aria-label="查看思考流程"
                    onClick={() => setShowLifecycle(true)}
                  >
                    <MoreHorizontal className="w-[15px] h-[15px]" strokeWidth={1.5} />
                  </button>
                  {(showLifecycle || lifecyclePinned) && (
                    <LifecycleHoverPanel
                      content={messageContent}
                      isRunning={isMessageRunning}
                      pinned={lifecyclePinned}
                      position={lifecyclePosition}
                      panelRef={lifecyclePanelRef}
                      onPinToggle={handleLifecyclePinToggle}
                      onDragStart={handleLifecycleDragStart}
                    />
                  )}
                </div>
                
                {/* Only show memory meter on the last message */}
                <AuiIf condition={(s) => s.message.isLast}>
                  <MemoryLimitUI messageCount={realMessageCount} />
                </AuiIf>
              </div>
            </AuiIf>
          </div>
        </AuiIf>
      </div>
    </MessagePrimitive.Root>
  );
};

const MemoryLimitUI = ({ messageCount }: { messageCount: number }) => {
  const progress = getConversationMemoryProgress(
    Array(messageCount).fill(null)
  );
  const percent = progress.percent;
  const strokeDasharray = 56.5;
  const strokeDashoffset = strokeDasharray * (1 - percent / 100);

  return (
    <div className="flex items-center gap-1.5 ml-1 pl-3 border-l border-black/10 dark:border-white/10 h-4">
      <div className="relative flex items-center justify-center w-3.5 h-3.5">
        <svg className="w-3.5 h-3.5 -rotate-90" viewBox="0 0 24 24">
          {/* Background circle */}
          <circle
            cx="12"
            cy="12"
            r="9"
            fill="none"
            stroke="currentColor"
            strokeWidth="3.5"
            className="opacity-20"
          />
          {/* Progress circle */}
          <circle
            cx="12"
            cy="12"
            r="9"
            fill="none"
            stroke="currentColor"
            strokeWidth="3.5"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            className="opacity-80 transition-[stroke-dashoffset,opacity] duration-200 ease-[var(--ease-out)]"
          />
        </svg>
      </div>
      <span className="text-[13px] font-medium text-[#444746] dark:text-[#c4c7c5]">
        {percent}%
      </span>
    </div>
  );
};
