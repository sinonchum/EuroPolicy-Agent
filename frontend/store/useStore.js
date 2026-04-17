import { create } from 'zustand';

/**
 * EPA Global State - RAM Optimized
 * 采用 Zustand 最小化组件重绘开销
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const useStore = create((set, get) => ({
  language: 'en',
  opportunities: [],
  selectedCountry: null,
  pulseTicker: [],
  evolutionData: null,
  isLoading: false,

  setLanguage: (lang) => set({ language: lang }),
  
  setSelectedCountry: (country) => {
    set({ selectedCountry: country });
    get().fetchData(get().language); // 切换国家立即刷新数据
  },
  
  fetchEvolution: async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/agent-evolution-status`);
      const data = await res.json();
      set({ evolutionData: data });
    } catch (err) {
      console.error("Evolution fetch failed", err);
    }
  },
  
  fetchData: async (lang) => {
    set({ isLoading: true });
    const { selectedCountry } = get();
    const url = new URL(`${API_BASE}/api/v1/opportunities`);
    url.searchParams.append("lang", lang);
    if (selectedCountry) url.searchParams.append("geo", selectedCountry);
    
    try {
      const res = await fetch(url.toString());
      const data = await res.json();
      set({ 
        opportunities: data.opportunities || [], 
        pulseTicker: data.pulse_ticker || [],
        isLoading: false 
      });
    } catch (err) {
      console.error("Fetch failed", err);
      set({ isLoading: false });
    }
  }
}));

export default useStore;
