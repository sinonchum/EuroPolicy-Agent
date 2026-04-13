'use client';

import React from 'react';
import useStore from '../store/useStore';

const LanguageSwitcher = () => {
    const { language, setLanguage, fetchData } = useStore();

    const langs = [
        { id: 'en', label: 'EN' },
        { id: 'zh', label: '中' },
        { id: 'fr', label: 'FR' },
        { id: 'de', label: 'DE' },
    ];

    const handleSwitch = (langId) => {
        setLanguage(langId);
        fetchData(langId); // 立即触发后端 API 刷新同步 AI 话术
    };

    return (
        <div className="flex bg-zinc-900 border border-zinc-800 rounded-lg p-1 gap-1">
            {langs.map((l) => (
                <button
                    key={l.id}
                    onClick={() => handleSwitch(l.id)}
                    className={`px-3 py-1 text-[10px] font-bold rounded transition-all ${
                        language === l.id 
                        ? 'bg-[#FFD700] text-black' 
                        : 'text-zinc-500 hover:text-zinc-200'
                    }`}
                >
                    {l.label}
                </button>
            ))}
        </div>
    );
};

export default LanguageSwitcher;
