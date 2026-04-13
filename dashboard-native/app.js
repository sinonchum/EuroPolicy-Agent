const TRANSLATIONS = {
    en: {
        nav_dashboard: "Dashboard",
        nav_copilot: "Copilot",
        nav_graph: "Knowledge Graph",
        nav_settings: "Settings",
        status_online: "System Live",
        search_placeholder: "Search directives or articles...",
        hero_title: "Policy Intelligence<br>at a Glance",
        hero_subtitle: "Real-time monitoring of EU regulatory landscape across energy, carbon and trade policies.",
        metric_directives: "Directives Tracked",
        metric_graph: "Graph Relations",
        metric_obligations: "Obligations",
        metric_risks: "Risks Mitigated",
        heatmap_title: "Industry Impact Heatmap",
        recent_title: "Recent Alerts",
        copilot_hero: "Compliance Copilot",
        copilot_subtitle: "Natural language engine powered by LangGraph to synthesize risks and strategies.",
        copilot_hint_title: "Suggested Queries",
        copilot_placeholder: "Ask about EU regulations...",
        copilot_button: "Analyze Scenario",
        copilot_step1: "Knowledge Graph Retrieval",
        copilot_step2: "Legal Expert Reasoning",
        copilot_step3: "Strategy Synthesis",
        copilot_legal_title: "Legal Analysis",
        copilot_sales_title: "Business Strategy",
        graph_hero: "Knowledge Graph",
        graph_subtitle: "A massive topological map of EU policy connectivity.",
        graph_placeholder_title: "Interactive Topology",
        graph_placeholder_desc: "Connect to Neo4j database to explore dynamic relationships.",
        hints: [
            "CBAM obligations 2026",
            "RED III contract adjustments",
            "Battery carbon footprint penalties",
            "AI Act compliance audit"
        ],
        legal_fallback: "Companies must begin full disclosure of carbon footprint emissions data in early 2026. If downstream suppliers default, they will face penalties equivalent to 3x the carbon price. Per CBAM Regulation (2023/956) Article 35, late reporting incurs a fine of €100 per tonne of CO₂.",
        strategy_fallback: "1. All contracts destined for the EU must include a mandatory 15% 'CBAM Risk Deposit' (fully refundable if no penalties are triggered).\n\n2. Transfer the carbon footprint reporting obligation to upstream battery/raw material suppliers, incorporated into force majeure and breach clauses.\n\n3. Add a 'Regulatory Change' clause allowing price adjustments due to EU regulatory amendments."
    },
    zh: {
        nav_dashboard: "控制面板",
        nav_copilot: "智能合规助手",
        nav_graph: "知识图谱",
        nav_settings: "设置",
        status_online: "系统在线",
        search_placeholder: "搜索法规或条款...",
        hero_title: "政策合规<br>态势感知",
        hero_subtitle: "实时监控覆盖能源、碳交易和贸易政策的欧盟法规变动。",
        metric_directives: "已监控指令",
        metric_graph: "图谱关系",
        metric_obligations: "法定义务",
        metric_risks: "风险拦截",
        heatmap_title: "行业影响热力图",
        recent_title: "最新预警",
        copilot_hero: "合规助手 Copilot",
        copilot_subtitle: "基于 LangGraph 的自然语言引擎，自动合规义务并生成应对策略。",
        copilot_hint_title: "建议提问",
        copilot_placeholder: "询问欧盟监管法规...",
        copilot_button: "启动深度推理",
        copilot_step1: "知识图谱拓扑检索",
        copilot_step2: "法律专家逻辑推理",
        copilot_step3: "商业策略自动合成",
        copilot_legal_title: "法律分析报告",
        copilot_sales_title: "商业应对策略",
        graph_hero: "知识图谱探索",
        graph_subtitle: "超大规模欧盟政策关联拓扑图。",
        graph_placeholder_title: "交互式拓扑预览",
        graph_placeholder_desc: "请连接 Neo4j 数据库以探索动态实体关系。",
        hints: [
            "2026年CBAM义务",
            "RED III合同调整",
            "电池碳足迹罚款",
            "AI法案合规审计"
        ],
        legal_fallback: "企业必须在 2026 年初开始全额披露碳足迹排放数据。如果下游供应商违约，将会承担相当于碳价 3 倍的巨额罚金。根据 CBAM 法规 (2023/956) 第35条，延迟申报将按每吨 CO₂ 100 欧元计算罚款。",
        strategy_fallback: "1. 所有发往欧盟的合同，必须强制添加 15% 的 'CBAM 风险保证金'（若未触发罚款则原路退还）。\n\n2. 将提供碳足迹报告义务转嫁给上游电池/原材料供应商，列入不可抗力和违约条款。\n\n3. 建议在合同中增加 '法规变更' 条款，允许因 EU 法规修订而调整价格。"
    },
    fr: {
        nav_dashboard: "Tableau de Bord",
        nav_copilot: "Copilote de Conformité",
        nav_graph: "Graphe de Connaissance",
        nav_settings: "Paramètres",
        status_online: "Système en Ligne",
        search_placeholder: "Rechercher des directives...",
        hero_title: "Intelligence<br>Réglementaire",
        hero_subtitle: "Surveillance en temps réel du paysage réglementaire de l'UE.",
        metric_directives: "Directives Suivies",
        metric_graph: "Relations Graphe",
        metric_obligations: "Obligations",
        metric_risks: "Risques Atténués",
        heatmap_title: "Carte de Chaleur d'Impact",
        recent_title: "Alertes Récentes",
        copilot_hero: "Copilote de Conformité",
        copilot_subtitle: "Moteur de langage naturel pour synthétiser les risques et les stratégies.",
        copilot_hint_title: "Suggestions",
        copilot_placeholder: "Posez votre question...",
        copilot_button: "Lancer l'Analyse",
        copilot_step1: "Récupération du Graphe",
        copilot_step2: "Raisonnement Juridique",
        copilot_step3: "Synthèse de Stratégie",
        copilot_legal_title: "Analyse Juridique",
        copilot_sales_title: "Stratégie Commerciale",
        graph_hero: "Graphe de Connaissance",
        graph_subtitle: "Une carte topographique massive de la connectivité des politiques de l'UE.",
        graph_placeholder_title: "Topologie Interactive",
        graph_placeholder_desc: "Connectez-vous à Neo4j pour explorer les relations.",
        hints: [
            "CBAM obligations 2026",
            "RED III contrats",
            "Pénalités carbone batterie"
        ],
        legal_fallback: "Les entreprises doivent divulguer l'empreinte carbone début 2026. Pénalités de 3x le prix du carbone en cas de défaut. Amende de 100€ par tonne de CO₂.",
        strategy_fallback: "1. Dépôt de garantie CBAM de 15%.\n2. Transfert de l'obligation aux fournisseurs.\n3. Clause changement réglementaire."
    },
    de: {
        nav_dashboard: "Dashboard",
        nav_copilot: "Compliance Copilot",
        nav_graph: "Wissensgraph",
        nav_settings: "Einstellungen",
        status_online: "System Aktiv",
        search_placeholder: "Suche nach Richtlinien...",
        hero_title: "Regulatorische<br>Intelligenz",
        hero_subtitle: "Echtzeit-Überwachung der EU-Regulierungslandschaft.",
        metric_directives: "Richtlinien",
        metric_graph: "Graphbeziehungen",
        metric_obligations: "Pflichten",
        metric_risks: "Risiken Minimiert",
        heatmap_title: "Branchen-Heatmap",
        recent_title: "Aktuelle Warnungen",
        copilot_hero: "Compliance Copilot",
        copilot_subtitle: "KI-Engine zur Synthese von Risiken und Strategien.",
        copilot_hint_title: "Beispiele",
        copilot_placeholder: "Stellen Sie eine Frage...",
        copilot_button: "Analyse Starten",
        copilot_step1: "Wissensgraph-Abfrage",
        copilot_step2: "Rechtliche Prüfung",
        copilot_step3: "Strategie-Erstellung",
        copilot_legal_title: "Rechtliche Analyse",
        copilot_sales_title: "Geschäftsstrategie",
        graph_hero: "Wissensgraph",
        graph_subtitle: "Eine topologische Karte der EU-Politik.",
        graph_placeholder_title: "Interaktive Topologie",
        graph_placeholder_desc: "Neo4j verbinden, um Beziehungen zu sehen.",
        hints: [
            "CBAM Pflichten 2026",
            "RED III Verträge",
            "Batterie-Strafe"
        ],
        legal_fallback: "Unternehmen müssen ab 2026 CO2-Daten offenlegen. Strafen bis zum 3-fachen CO2-Preis. Verspätete Meldung: 100€/Tonne CO2.",
        strategy_fallback: "1. 15% CBAM-Risikokaution.\n2. Meldepflicht auf Lieferanten übertragen.\n3. Klausel für regulatorische Änderungen."
    }
};

let currentLang = 'en';

document.addEventListener('DOMContentLoaded', () => {
    // === Initialize Icons ===
    lucide.createIcons();

    // === Multi-language Logic ===
    const langSelect = document.getElementById('langSelect');
    
    function updateI18n() {
        // Text nodes
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (TRANSLATIONS[currentLang][key]) {
                el.innerHTML = TRANSLATIONS[currentLang][key];
            }
        });
        
        // Placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (TRANSLATIONS[currentLang][key]) {
                el.placeholder = TRANSLATIONS[currentLang][key];
            }
        });

        // Update hints
        renderHints();
        // Update charts
        renderHeatmap();
        // Update activities
        renderActivities();
    }

    langSelect.addEventListener('change', (e) => {
        currentLang = e.target.value;
        document.documentElement.lang = currentLang;
        updateI18n();
    });

    // === Navigation ===
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const target = item.getAttribute('data-target');
            pages.forEach(p => {
                if (p.id === target) {
                    p.classList.add('active');
                } else {
                    p.classList.remove('active');
                }
            });

            if (target === 'dashboard') {
                setTimeout(renderHeatmap, 100);
            }
        });
    });

    // === Charts (Plotly) ===
    function renderHeatmap() {
        const labels = currentLang === 'zh' ? 
            ['CBAM税', '新能源', '电池法', '环设', 'AI法'] : 
            ['CBAM', 'Energy', 'Battery', 'EcoDesign', 'AI Act'];
        
        const industries = currentLang === 'zh' ? 
            ['钢铁铝业', '光伏组件', '汽车制造'] : 
            ['Steel', 'Solar', 'Auto'];

        const data = [{
            z: [[60, 10, 30, 80, 5], [15, 5, 90, 20, 40], [40, 70, 45, 10, 85]],
            x: labels,
            y: industries,
            type: 'heatmap',
            colorscale: [
                [0, '#f1f5f9'],
                [0.5, '#3b82f6'],
                [1, '#7c3aed']
            ],
            showscale: false
        }];

        const layout = {
            margin: { t: 0, l: 80, r: 0, b: 30 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { family: 'Outfit, Noto Sans SC', size: 12, color: '#64748b' }
        };

        Plotly.newPlot('heatmapContainer', data, layout, {displayModeBar: false, responsive: true});
    }

    // === Activity Feed ===
    function renderActivities() {
        const feed = document.getElementById('activityFeed');
        const items = currentLang === 'zh' ? [
            { id: 1, title: "CBAM 法规生效", desc: "Article 35 进入全面合规期", color: "red" },
            { id: 2, title: "RED III 时间表更新", desc: "成员国转化截止日期变更", color: "blue" },
            { id: 3, title: "电池碳足迹声明", desc: "新格式文档已在 Cellar 发布", color: "purple" }
        ] : [
            { id: 1, title: "CBAM Enforcement", desc: "Article 35 enters full compliance", color: "red" },
            { id: 2, title: "RED III Timeline", desc: "Transposition deadline shifted", color: "blue" },
            { id: 3, title: "Battery Carbon Format", desc: "New format published on Cellar", color: "purple" }
        ];

        feed.innerHTML = items.map(item => `
            <div class="activity-item">
                <div class="act-indicator ${item.color}"></div>
                <div class="act-info">
                    <h5>${item.title}</h5>
                    <p>${item.desc}</p>
                </div>
            </div>
        `).join('');
    }

    // === Copilot Simulation ===
    function renderHints() {
        const container = document.getElementById('hintItems');
        const hints = TRANSLATIONS[currentLang].hints;
        container.innerHTML = hints.map(hint => `
            <div class="hint-pill">${hint}</div>
        `).join('');
        
        container.querySelectorAll('.hint-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                document.getElementById('copilotQuery').value = pill.innerText;
            });
        });
    }

    const runBtn = document.getElementById('runBtn');
    runBtn.addEventListener('click', async () => {
        const stage = document.getElementById('analysisStage');
        const results = document.getElementById('resultGrid');
        const steps = document.querySelectorAll('.step');
        
        // UI Reset
        results.classList.add('hidden');
        stage.classList.remove('hidden');
        runBtn.disabled = true;

        for (let i = 0; i < steps.length; i++) {
            steps[i].classList.add('active');
            await new Promise(r => setTimeout(r, 800));
            if (i < steps.length - 1) steps[i].classList.remove('active');
        }

        stage.classList.add('hidden');
        results.classList.remove('hidden');
        runBtn.disabled = false;

        document.getElementById('legalText').innerText = TRANSLATIONS[currentLang].legal_fallback;
        document.getElementById('strategyText').innerText = TRANSLATIONS[currentLang].strategy_fallback;

        // Visual scroll down
        document.querySelector('.scroll-container').scrollBy({ top: 300, behavior: 'smooth' });
    });

    // Initial Render
    updateI18n();
});
