'use client';

import React, { useEffect } from 'react';
import dynamic from 'next/dynamic';
import useStore from '../store/useStore';
import LanguageSwitcher from '../components/LanguageSwitcher';
import PulseTicker from '../components/PulseTicker';
import LeadCardList from '../components/LeadCardList';
import EvolutionPanel from '../components/EvolutionPanel';
import ImpactAlert from '../components/ImpactAlert';
import { LayoutGrid, Compass, ShieldCheck } from 'lucide-react';

// 动态加载 heavy 图表组件处理 8G RAM 优化
const OpportunityRadar = dynamic(() => import('../components/OpportunityRadar'), { 
    ssr: false,
    loading: () => <div className="h-[300px] w-full bg-zinc-900 animate-pulse rounded-xl" />
});

export default function BloombergDashboard() {
    const { language, fetchData } = useStore();

    useEffect(() => {
        fetchData(language);
        // 设置一个背景同步，模拟 GEP 运行
        const interval = setInterval(() => fetchData(language), 60000);
        return () => clearInterval(interval);
    }, [language]);

    const i18n = {
        en: { headline: "Market Intelligence Terminal", leads_title: "Active Opportunities", overview: "Policy Overview" },
        zh: { headline: "市场情报决策终端", leads_title: "活跃获客商机", overview: "政策态势一览" },
        fr: { headline: "Terminal d'Intelligence Marché", leads_title: "Opportunités Actives", overview: "Aperçu de la Politique" },
        de: { headline: "Marktintelligenz-Terminal", leads_title: "Aktive Verkaufschancen", overview: "Politik-Übersicht" }
    }[language] || i18n.en;

    return (
        <div className="min-h-screen bg-[#050505] text-zinc-300 font-sans selection:bg-amber-500 selection:text-black">
            {/* Top Bar */}
            <header className="border-b border-zinc-800 bg-[#0A0A0A] px-6 py-3 flex justify-between items-center sticky top-0 z-40 backdrop-blur-md">
                <div className="flex items-center gap-4">
                    <div className="bg-red-600 px-2 py-0.5 text-[10px] font-black italic rounded text-white tracking-tighter">EPA LIVE</div>
                    <h1 className="text-sm font-bold tracking-tight text-white uppercase">{i18n.headline}</h1>
                </div>
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2 text-[10px] text-zinc-500 font-mono">
                        <ShieldCheck size={12} className="text-[#00FF41]" />
                        ZERO-OPS SECURE
                    </div>
                    <LanguageSwitcher />
                </div>
            </header>

            {/* Pulse Ticker */}
            <PulseTicker />

            <main className="max-w-[1600px] mx-auto p-6 grid grid-cols-12 gap-6">
                
                {/* Left Column: Intelligence Base (3col) */}
                <div className="col-span-12 lg:col-span-3 space-y-6">
                    <div className="p-4 border border-zinc-800 rounded-xl bg-gradient-to-br from-zinc-900 to-[#0A0A0A]">
                         <div className="flex items-center gap-2 text-xs font-bold text-zinc-400 mb-4 uppercase">
                            <Compass size={14} className="text-[#FFD700]" /> {i18n.overview}
                         </div>
                         <div className="h-[350px]">
                            <OpportunityRadar />
                         </div>
                    </div>
                    
                    <EvolutionPanel />
                </div>

                {/* Center Column: Lead Radar (6col) */}
                <div className="col-span-12 lg:col-span-6 space-y-4">
                    <div className="flex items-center justify-between mb-2">
                         <div className="flex items-center gap-2 text-xs font-bold text-zinc-400 uppercase">
                            <LayoutGrid size={14} /> {i18n.leads_title}
                         </div>
                         <span className="text-[10px] font-mono text-zinc-600">FILTER: [ALL_SECTORS]</span>
                    </div>
                    <LeadCardList />
                </div>

                {/* Right Column: Execution Insights (3col) - Placeholder for now */}
                <div className="col-span-12 lg:col-span-3">
                    <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl p-6 h-full border-dashed flex flex-col items-center justify-center text-center opacity-40">
                        <div className="text-zinc-600 mb-2 font-mono text-[10px]">EXECUTION_STRATEGY_VIEW</div>
                        <p className="text-[10px] text-zinc-700">Connect to Salesforce/Hubspot for direct conversion tracking.</p>
                    </div>
                </div>

            </main>

            {/* Global Warning Overlay */}
            <ImpactAlert originalScore={95} newScore={72} />

            {/* Footer Status */}
            <footer className="fixed bottom-0 w-full px-6 py-2 bg-black/80 border-t border-zinc-900 flex justify-between items-center z-40">
                <div className="text-[9px] font-mono text-zinc-600 uppercase tracking-widest flex items-center gap-4">
                    <span>Node: Local_EPA_Instance_v3</span>
                    <span className="text-[#00FF41]">● Latency: 12ms</span>
                </div>
                <div className="text-[9px] font-mono text-zinc-800">
                    &copy; 2026 EUROPOLICY AGENT SYSTEM
                </div>
            </footer>
        </div>
    );
}
