# Substation by K

## Operational Intelligence for Digital Substations

> **"Da comunicação ao diagnóstico."**

A plataforma de inteligência operacional que transforma dados de automação, proteção e comunicação em **diagnóstico, histórico, evidências e recomendações de ação** para subestações digitais.

---

## 🚀 Visão Geral

**Substation by K** não é apenas mais um analisador de protocolos IEC 61850. É uma **plataforma de inteligência operacional** que entende o contexto da subestação, identifica padrões, diagnostica problemas e fornece recomendações baseadas em evidências.

### 🎯 Proposta de Valor

| O que o mercado oferece | O que oferecemos |
|------------------------|------------------|
| Visualização de pacotes | **Diagnóstico com evidências** |
| Análise de protocolos | **Inteligência operacional** |
| Ferramentas de teste | **Memória histórica da subestação** |
| Monitoramento isolado | **Digital Twin + Análise preditiva** |

---

## 📊 Business Plan

### 1. Modelo de Negócio

#### Produtos

| Produto | Público Alvo | Modelo Comercial | Recursos |
|---------|-------------|------------------|----------|
| **K-Integrator** | Integradoras, O&M | Assinatura + Projetos | Diagnóstico, comissionamento, relatórios |
| **K-Utility** | Concessionárias | Assinatura anual por subestação | Monitoramento contínuo, Digital Twin, histórico |
| **K-Lab** | Fabricantes, laboratórios | Licença corporativa | Testes, simulação, validação |

#### Preços (Estimativa Inicial)

- **K-Integrator**: R$ 20.000 - R$ 50.000/ano + R$ 5.000 - R$ 15.000 por projeto
- **K-Utility**: R$ 15.000 - R$ 30.000/subestação/ano
- **K-Lab**: R$ 100.000 - R$ 250.000/ano (corporativo)

### 2. Estratégia de Mercado

#### Fases de Lançamento

```
Fase 1 (0-12 meses): K-Integrator
├── MVP: K-Diagnosis + K-Reports
├── Clientes: 5-10 integradoras
├── Subestações: 20-50
└── Faturamento: R$ 500K - R$ 1M

Fase 2 (12-24 meses): K-Utility
├── Versão completa: 5 módulos
├── Clientes: 3-5 concessionárias
├── Subestações: 50-100
└── Faturamento: R$ 1M - R$ 3M

Fase 3 (24-36 meses): K-Lab + Expansão
├── Produto corporativo
├── Clientes: Fabricantes globais
├── Subestações: 100+
└── Faturamento: R$ 3M - R$ 10M
```

#### Canais de Venda

1. **Venda Direta**: Equipe comercial para grandes clientes
2. **Parcerias**: Colaboração com fabricantes de IEDs
3. **Distribuição**: Integradoras como revendedoras
4. **Digital**: Site, webinars, whitepapers

### 3. Custos Iniciais

| Item | Custo (R$) | Período |
|------|------------|---------|
| Desenvolvimento MVP | 200.000 | 6 meses |
| Equipe técnica (3 devs) | 30.000/mês | Contínuo |
| Infraestrutura cloud | 5.000/mês | Contínuo |
| Marketing | 15.000/mês | Contínuo |
| Vendas | 20.000/mês | Contínuo |
| **Total Ano 1** | **500.000** | - |

### 4. Projeção de Receita (3 anos)

| Ano | Clientes | Subestações | Receita (R$) | Lucro (R$) |
|-----|----------|-------------|--------------|------------|
| 1 | 10 | 30 | 1.500.000 | -200.000 |
| 2 | 25 | 80 | 4.000.000 | 1.200.000 |
| 3 | 50 | 150 | 8.000.000 | 3.500.000 |

---

## 🏗️ Arquitetura do Produto

### Módulos Principais

```
┌─────────────────────────────────────────────────────────────┐
│                    SUBSTATION BY K                            │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ K-Discover  │  │K-Digital Twin│  │      K-Diagnosis      │  │
│  │   (v1.1)    │  │    (v1.2)    │  │       (v1.0)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  K-Guardian │  │  K-Reports   │  │       K-AI           │  │
│  │   (v1.3)    │  │    (v1.0)    │  │      (v2.0)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

### MVP (v1.0)

**Módulos Iniciais:**
- ✅ K-Diagnosis (Coração do produto)
- ✅ K-Reports (Gerador de relatórios)

**Funcionalidades MVP:**
1. Importar SCD/CID/ICD
2. Capturar/analisar tráfego de rede
3. Mapear caminho dos sinais
4. Gerar diagnóstico + relatório

### Roadmap de Versões

| Versão | Módulos | Previsão | Status |
|--------|---------|----------|--------|
| v1.0 | K-Diagnosis, K-Reports | Q1 2025 | 🚀 Em desenvolvimento |
| v1.1 | +K-Discover | Q2 2025 | 📅 Planejado |
| v1.2 | +K-Digital Twin | Q3 2025 | 📅 Planejado |
| v1.3 | +K-Guardian | Q4 2025 | 📅 Planejado |
| v2.0 | +K-AI, Substation Memory™ | Q2 2026 | 📅 Planejado |

---

## 🔧 Módulos Detalhados

### 1. K-Discover (Descoberta Automática)

**Objetivo:** Mapear automaticamente toda a topologia da subestação.

**Funcionalidades:**
- Descoberta de IEDs, switches, gateways, RTUs, SCADA
- Identificação de protocolos: GOOSE, MMS, Sampled Values, IEC-104, DNP3, SNMP, PTP, PRP
- Mapeamento de IPs, MACs, VLANs
- Verificação de sincronismo
- Geração de mapa vivo da subestação

**Tecnologias:**
- Network scanning (ARP, ICMP, SNMP)
- Protocol parsing (libiec61850, libpcap)
- Topology inference algorithms

### 2. K-Digital Twin (Gêmeo Digital)

**Objetivo:** Manter uma representação digital precisa da arquitetura esperada vs. real.

**Funcionalidades:**
- Importação de SCD/CID/ICD
- Comparação: Projeto × Configuração × Rede real
- Detecção de divergências
- Visualização 3D/interativa
- Simulação de cenários

**Diferencial:** Substation Memory™ - Histórico completo de mudanças

### 3. K-Diagnosis (Diagnóstico Inteligente)

**Objetivo:** Responder: O que aconteceu? Onde? Por quê?

**Funcionalidades:**
- Análise de caminho de sinais (signal path tracing)
- Identificação de pontos de falha
- Probabilidade de causas
- Evidências para cada hipótese
- Recomendações de ação

**Exemplo de Saída:**
```
Evento: SCADA perdeu posição do disjuntor Q01

Diagnóstico:
├── Probabilidade de falha no gateway: 85%
│   └── Evidências:
│       ├── IED continua publicando estado
│       ├── GOOSE está presente
│       ├── Switch registra tráfego
│       ├── Comunicação IED→gateway ativa
│       ├── Ponto não observado no IEC-104
│       └── Última configuração: gateway (2024-11-15)
└── Próximos passos:
    1. Verificar mapeamento IEC-104 no gateway
    2. Checar logs do gateway
    3. Testar conectividade com SCADA
```

### 4. K-Guardian (Governança e Integridade)

**Objetivo:** Monitorar mudanças e garantir integridade da configuração.

**Funcionalidades:**
- Baseline da subestação (estado homologado)
- Detecção de mudanças em tempo real
- Registro de alterações (quando, onde, o que, impacto)
- Alertas de não-conformidade
- Histórico de versões

### 5. K-Reports (Relatórios Automáticos)

**Objetivo:** Eliminar horas de trabalho manual em documentação.

**Tipos de Relatórios:**
- **FAT**: Relatório de testes de fábrica
- **SAT**: Relatório de comissionamento
- **O&M**: Relatório de saúde da subestação
- **Incidente**: Análise de problemas
- **Auditoria**: Histórico de alterações
- **Engenharia**: Comparação projeto × real

### 6. K-AI (Inteligência Artificial)

**Objetivo:** Diagnóstico assistido por evidências.

**Funcionalidades:**
- Análise de eventos históricos
- Identificação de padrões
- Geração de hipóteses com evidências
- Recomendações baseadas em casos anteriores
- Substation Memory™: Base de conhecimento da subestação

**Diferencial:** A IA **explica** suas conclusões com dados concretos.

---

## 🎯 Diferenciais Competitivos

### 1. Substation Memory™

**O que é:** Base de conhecimento histórica da subestação.

**Benefícios:**
- Aprende com problemas passados
- Identifica padrões recorrentes
- Fornece soluções que funcionaram antes
- Cria uma "memória institucional" digital

### 2. Agnosticismo de Fabricante

**Suporte a:**
- SEL, Siemens, Schneider, GE, ABB, WEG, e outros
- IEC 61850, IEC-104, DNP3, Modbus, SNMP, PTP, PRP

**Vantagem:** Não compete com fabricantes, **complementa** seus sistemas.

### 3. Arquitetura Híbrida (Edge + Cloud)

```
┌─────────────────────────────────────────────────────────────┐
│                        NUVEM (Cloud)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   K-AI          │  │  K-Reports       │  │  Dashboard   │  │
│  │  (Análise)      │  │  (Geração)       │  │  (Visualização)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       EDGE (Na subestação)                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ K-Discover      │  │ K-Diagnosis      │  │ K-Guardian   │  │
│  │ K-Digital Twin   │  │ (Processamento)   │  │ (Monitoramento)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    REDE OT (Tempo Real)                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │
│  │  IEDs   │  │ Switches │  │ Gateways │  │   SCADA     │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Vantagens:**
- Processamento sensível permanece na rede OT (segurança)
- Baixa latência para diagnóstico em tempo real
- Escalabilidade com a nuvem

### 4. Enfoque em Evidências

**Não dizemos:** "O problema é o gateway"

**Dizemos:** "O problema provavelmente é o gateway porque:
1. O IED está publicando o sinal corretamente (evidência: pacotes GOOSE)
2. O switch registra tráfego até o gateway (evidência: logs SNMP)
3. O gateway não encaminha para o SCADA (evidência: ausência em IEC-104)
4. A última configuração foi no gateway (evidência: histórico de mudanças)"

---

## 🛠️ Tecnologias e Implementação

### Backpropagation e Feedforward para Processamento de Dados

O sistema utiliza técnicas de **backpropagation** (retropropagação) e **feedforward** (alimentação direta) para:

1. **Backpropagation (Análise de Falhas):**
   - Rastrear o caminho inverso de sinais com falha
   - Identificar pontos de quebra na cadeia de comunicação
   - Calcular probabilidades de causas

2. **Feedforward (Otimização):**
   - Prever impactos de mudanças de configuração
   - Simular cenários antes da implementação
   - Otimizar rotas de comunicação

### Arquitetura de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DE DADOS                             │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  Captura de Dados → Processamento → Análise → Diagnóstico      │
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Network    │    │  Backprop   │    │  Feedforward │      │
│  │  Sniffer    │───▶│  Engine     │───▶│  Engine     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                       │                                       │
│                       ▼                                       │
│                  ┌─────────────┐                              │
│                  │  Knowledge   │                              │
│                  │  Graph       │                              │
│                  └─────────────┘                              │
│                       │                                       │
│                       ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                SUBSTATION MEMORY™                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

### Stack Tecnológica

| Camada | Tecnologias |
|--------|-------------|
| **Captura** | libpcap, Wireshark, tshark |
| **Protocolos** | libiec61850, libdnp3, libmodbus |
| **Processamento** | Python, C++, Rust |
| **Backpropagation** | TensorFlow/PyTorch (para análise de padrões) |
| **Feedforward** | Graph algorithms, simulation engines |
| **Armazenamento** | PostgreSQL, TimescaleDB, Elasticsearch |
| **Visualização** | React, D3.js, Three.js |
| **Edge** | Docker, Kubernetes (Edge), Raspberry Pi/Industrial PCs |
| **Cloud** | AWS/Azure/GCP, Kubernetes |

---

## 📈 Métricas de Sucesso

### Para o Cliente

- ⏱️ **Redução de tempo de diagnóstico**: 70-90%
- 💰 **Economia em horas de engenharia**: 50-70%
- 📊 **Aumento de disponibilidade**: 1-3%
- 📝 **Tempo de geração de relatórios**: 90% mais rápido

### Para o Negócio

- 🎯 **Taxa de conversão MVP**: 20-30%
- 💵 **Ticket médio**: R$ 20.000 - R$ 50.000/ano por subestação
- 📈 **Crescimento anual**: 100-200%
- 🏆 **NPS (Net Promoter Score)**: 50+

---

## 🌍 Mercado e Concorrência

### Análise Competitiva

| Competidor | Produto | Pontos Fortes | Pontos Fracos | Nosso Diferencial |
|------------|---------|---------------|---------------|-------------------|
| OMICRON | StationScout | Visão abrangente, diagnóstico | Foco em teste, não em inteligência operacional | **Inteligência + Histórico + Evidências** |
| Conprove | SV/GOOSE Monitor | Monitoramento local, bom para SV | Limitado a protocolos específicos | **Multi-protocolo + Digital Twin + AI** |
| Siemens | SICAM | Integração com seus equipamentos | Proprietário, limitado a seu ecossistema | **Agnóstico + Substation Memory™** |
| SEL | SEL-5030 | Análise de protocolos | Focado em seus próprios IEDs | **Independente de fabricante** |

### Barreiras de Entrada

1. **Conhecimento especializado**: IEC 61850 e sistemas de automação
2. **Base instalada**: Clientes já usam soluções existentes
3. **Certificações**: Requisitos para sistemas críticos

### Nossas Vantagens

1. **Enfoque único**: Inteligência operacional, não apenas monitoramento
2. **Agnosticismo**: Funciona com qualquer fabricante
3. **Substation Memory™**: Barreira competitiva única
4. **Modelo de negócio flexível**: Adapta-se a diferentes clientes

---

## 🎯 Estratégia de Lançamento

### Passos Imediatos

1. **Finalizar MVP (3 meses)**
   - K-Diagnosis (análise de caminho de sinais)
   - K-Reports (geração de relatórios básicos)
   - Interface web simples

2. **Testes com Early Adopters (2 meses)**
   - 3-5 integradoras parceiras
   - 10-20 subestações piloto
   - Feedback e ajustes

3. **Lançamento Oficial (Mês 6)**
   - Site e materiais de marketing
   - Webinars e whitepapers
   - Parcerias com fabricantes

### Clientes Ideais para MVP

1. **Integradoras de automação** (Prioridade 1)
   - Sentem a dor de diagnóstico rápido
   - Podem usar em múltiplos projetos
   - Ciclo de venda mais curto

2. **Empresas de O&M** (Prioridade 2)
   - Necessidade de monitoramento contínuo
   - Valorizam histórico e relatórios

3. **Concessionárias inovadoras** (Prioridade 3)
   - Dispostas a testar novas tecnologias
   - Têm múltiplas subestações

---

## 💡 Próximos Passos

### Curto Prazo (1-3 meses)

- [x] Definir escopo do MVP
- [x] Criar Business Plan
- [ ] Desenvolver K-Diagnosis (core)
- [ ] Implementar backpropagation para análise de falhas
- [ ] Criar gerador de relatórios (K-Reports)
- [ ] Testar com dados reais de subestações

### Médio Prazo (3-6 meses)

- [ ] Lançar MVP para early adopters
- [ ] Desenvolver K-Discover
- [ ] Implementar Digital Twin básico
- [ ] Criar dashboards de visualização
- [ ] Estabelecer primeiras parcerias

### Longo Prazo (6-12 meses)

- [ ] Lançar versão completa (v1.3)
- [ ] Adicionar K-AI e Substation Memory™
- [ ] Expandir para mercado internacional
- [ ] Criar programa de certificação

---

## 📞 Contato

Para mais informações sobre o **Substation by K**:

- **Website**: [substationbyk.com](https://substationbyk.com) (em desenvolvimento)
- **Email**: contact@substationbyk.com
- **LinkedIn**: [Substation by K](https://linkedin.com/company/substationbyk)

---

## 📄 Documentação Adicional

- [Plano Técnico Detalhado](docs/technical/technical_plan.md)
- [Arquitetura do Sistema](docs/architecture/system_architecture.md)
- [Especificações dos Módulos](docs/modules/)
- [Estratégia de Marketing](docs/business/marketing_strategy.md)
- [Modelo Financeiro](docs/business/financial_model.md)

---

> **"Transformando dados em inteligência operacional para subestações digitais."**

*Substation by K - v1.0 | Business Plan | Última atualização: Novembro 2024*
