'use client';

import React, { useEffect } from 'react';
import useStore from '../store/useStore';
import { BrainCircuit, Milestone, Layers } from 'lucide-react';

const EvolutionPanel = () => {
    const { evolutionData, fetchEvolution, language } = useStore();

    useEffect(() => {
        fetchEvolution();
        const interval = setInterval(fetchEvolution, 30000); // 每 30 秒轮询一次进化状态
        return () => clearInterval(interval);
    }, []);

    const t = {
        en: { title: "Agent Evolution", milestone: "Milestone", depth: "Memory Depth", logic: "Pivoted Logic" },
        zh: { title: "智能体自主进化", milestone: "关键里程碑", depth: "记忆深度", logic: "动态修正逻辑" },
        fr: { title: "Évolution de l'Agent", milestone: "Jalon Clé", depth: "Profondeur Mémoire", logic: "Logique Pivot" },
        de: { title: "Agenten-Evolution", milestone: "Meilenstein", depth: "Gedächtnistiefe", logic: "Pivot-Logik" }
    }[language] || t.en;

    if (!evolutionData) return null;

    return (
        <div className="bg-[#0D0D0D] border border-zinc-800 rounded-xl p-5 shadow-inner">
            <div className="flex items-center gap-3 mb-4">
                <div className="bg-amber-500/10 p-2 rounded-lg text-amber-500">
                    <BrainCircuit size={20} className="animate-pulse" />
                </div>
                <div>
                    <h3 className="text-zinc-200 text-xs font-black uppercase tracking-widest">{t.title}</h3>
                    <p className="text-[10px] text-zinc-600 font-mono">NEURAL ADAPTATION ACTIVE</p>
                </div>
            </div>

            <div className="space-y-4">
                <div className="space-y-1">
                    <div className="flex items-center gap-2 text-[10px] text-zinc-500 font-bold uppercase">
                        <Milestone size={12} /> {t.milestone}
                    </div>
                    <p className="text-amber-400 text-xs font-bold bg-amber-500/5 p-2 rounded border border-amber-500/10">
                        {evolutionData.learning_milestone}
                    </p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1">
                        <div className="text-[10px] text-zinc-500 font-bold uppercase">{t.depth}</div>
                        <div className="text-zinc-300 text-xs font-mono">{evolutionData.memory_depth}</div>
                    </div>
                    <div className="space-y-1">
                        <div className="text-[10px] text-zinc-500 font-bold uppercase">Prompt Ver.</div>
                        <div className="text-zinc-500 text-[10px] font-mono truncate">v3.0.0-evolved</div>
                    </div>
                </div>

                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-[10px] text-zinc-500 font-bold uppercase">
                        <Layers size={12} /> {t.logic}
                    </div>
                    <ul className="flex flex-wrap gap-2">
                        {evolutionData.weights_pivoted.map((w, i) => (
                            <li key={i} className="bg-zinc-900 border border-zinc-800 px-2 py-1 rounded text-[9px] text-zinc-400 font-mono">
                                {w}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default EvolutionPanel;
